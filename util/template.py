# -*- coding: utf-8 -*-

import os

from jinja2 import Environment,PrefixLoader,FileSystemLoader,FunctionLoader
from settings import DEBUG,ADMIN_TEMPLATE_DIR,THEME_TEMPLATE_DIR
from util import filters

from blog.models import Blog

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

loader = PrefixLoader({
    'theme': FunctionLoader(load_theme),
    'admin': FileSystemLoader(ADMIN_TEMPLATE_DIR),
})
env = Environment(loader=loader,auto_reload=DEBUG)
env.filters['date'] = filters.datetimeformat

def render(template, **kwargs):
    """渲染模板"""
    t = env.get_template(template)
    return t.render(**kwargs)
