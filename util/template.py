# -*- coding: utf-8 -*-

import os
import logging

from google.appengine.api import memcache

from jinja2 import Environment,PrefixLoader,FileSystemLoader,FunctionLoader
# from jinja2 import MemcachedBytecodeCache
from settings import DEBUG,ADMIN_TEMPLATE_DIR,THEME_TEMPLATE_DIR
from util import filters

from blog.models import Blog, blog
from theme.models import ThemeFile

class PerformancePrefixLoader(PrefixLoader):
    """加强缓存，模板加载系统"""
    def load(self, environment, name, globals=None):
        """Loads a Python code template"""
        if DEBUG:
            return super(PerformancePrefixLoader, self) \
                        .load(environment, name, globals)
        if globals is None:
            globals = {}
        theme = blog.theme
        memcache_key = 'template_%s_%s' % (theme, name)
        code = memcache.get(memcache_key)
        if code is None:
            logging.info("oops no memcache!!")
            source, filename, uptodate = self.get_source(environment, name)
            code = environment.compile(source, raw=True)
            memcache.set(memcache_key, code)
            logging.info(name)
        else:
            logging.info("yeh memcache")
            uptodate = lambda: False
        code = compile(code, name, 'exec')
        return environment.template_class.from_code(environment, code,
                                                    globals, uptodate)

def load_theme(name):
    """加载自定义模板,优先扫描数据库数据,而后扫描本地文件"""
    theme = blog.theme
    
    theme_path = os.path.join(THEME_TEMPLATE_DIR, theme)
    if os.path.isdir(theme_path):
        try:
            filename = os.path.join(theme_path, name)
            f = open(filename)
            source = f.read().decode('utf-8')
            f.close()
        except IOError:
            source = None
    else:
        theme_file_query = ThemeFile.all().filter('theme_name =', theme)
        theme_file_query.filter('filename =', name)
        theme_file_query.filter('filetype =', 'template')
        theme_file = theme_file_query.get()

        if not theme_file:
            logging.info('no template')
            source = None
        else:
            source = theme_file.filecontent.decode('utf-8')
    return source, None, lambda: False

loader = PerformancePrefixLoader({
    'theme': FunctionLoader(load_theme),
    'admin': FileSystemLoader(ADMIN_TEMPLATE_DIR),
})
# bcc = MemcachedBytecodeCache(memcache)

env = Environment(loader=loader,auto_reload=DEBUG)
env.filters['date'] = filters.datetimeformat

def render(template, **kwargs):
    """渲染模板"""
    t = env.get_template(template)
    return t.render(**kwargs)
