# -*- coding: utf-8 -*-

import logging

from util.template import env
import simplejson as json

from blog.models import Blog, Widget

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
    
    def header(self):
        """前台博客通用Header"""
        header = []
        header.append('<link rel="alternate" type="application/rss+xml" href="/feed" />')
        header.append(self.custom_header)
        
        return '\n'.join(header)
    
    def sidebar(self, number='1'):
        """侧边条应用"""
        number = unicode(number)
        
        blog = Blog.get()
        if blog.theme_widget:
            theme_widget = json.loads(blog.theme_widget)
            
            if theme_widget.has_key(number):
                setting = theme_widget.get(number)
                if setting:
                    return SidebarWidget(setting)
        
        return []

class SidebarWidget(object):
    """侧边条装饰，加载调用类"""
    
    next_value = 0
    
    def __init__(self, setting):
        self.setting = setting
    
    def __iter__(self):
        return self
    
    def next(self):
        try:
            ret = self.setting[self.next_value]
            self.next_value = self.next_value + 1
            
            widget_name = ret.get('name')
            widget = Widget.all().filter('name =', widget_name).get()
            widget = widget.item()
            
            return widget
        except:
            raise StopIteration
