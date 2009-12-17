# -*- coding: utf-8 -*-

import os
import base64, logging

from google.appengine.api import memcache

from jinja2 import Environment,PrefixLoader,FileSystemLoader,FunctionLoader
# from jinja2 import MemcachedBytecodeCache
from settings import DEBUG,ADMIN_TEMPLATE_DIR,THEME_TEMPLATE_DIR
from util import filters

from blog.models import Blog

try:
    mydata
except NameError:
    logging.error("damn")
    mydata = {}

def get_data_by_name(name):
    if base64.b64encode(name) in mydata:
        return mydata[base64.b64encode(name)]
    return None

class PerformancePrefixLoader(PrefixLoader):
    """加强缓存，模板加载系统"""
    def load(self, environment, name, globals=None):
        """Loads a Python code template"""
        if globals is None:
            globals = {}
        #try for a variable cache
        code = get_data_by_name(name)
        if code is not None:
            logging.info("ultrafast memcache")
        else:
            logging.info("slow memcache")
            code = memcache.get(name)
            if code is None:
                logging.info("oops no memcache!!")
                source, filename, uptodate = self.get_source(environment, name)
                # template = file(filename).read().decode('ascii').decode('utf-8')
                code = environment.compile(source, raw=True)
                memcache.set(name,code)
                logging.info(name)
            else:
                logging.info("yeh memcache")
            code = compile(code, name, 'exec')
            mydata[base64.b64encode(name)] = code
        return environment.template_class.from_code(environment, code,globals)
    
def load_theme(name):
    """加载自定义模板,优先扫描数据库数据,而后扫描本地文件"""
    theme = Blog.get().theme
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
        source = None
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
