# -*- coding: utf-8 -*-

from util.template import env

from blog.models import Blog

class BaseFront(object):
    """前台博客页面基本参数"""
    def __init__(self):
        env.globals['blog'] = Processor()
    

class Processor(object):
    """处理前台变量"""
    @property
    def info(self):
        return Blog.get()
    
    def __getattr__(self, name):
        """获取博客属性"""
        blog = Blog.get()
        return getattr(blog, name)
    
    def sidebar(self, name='default'):
        pass
