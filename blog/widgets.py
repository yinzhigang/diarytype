# -*- coding: utf-8 -*-

from StringIO import StringIO

from post.models import Post
from category.models import Category

class Widget(object):
    """博客装饰"""
    params = None
    
    def __init__(self, params=None):
        self.params = params
    
    def name(self):
        pass

class categories(Widget):
    """文章分类装饰"""
    key_name = 'categories'
    def name(self):
        return u"文章分类"
    
    def body(self):
        category_list = Category.all().order('sort')
        
        content = []
        write = content.append
        write('<ul>')
        for category in category_list:
            write('<li><a href="%s">%s</a></li>' % ('#', category.name))
        write('</ul>')
        
        return ''.join(content)

class recent_entries(Widget):
    """最新文章装饰"""
    key_name = 'recent_entries'
    def name(self):
        return u"最新文章"
    
    def body(self):
        post_list = Post.all().filter('hidden =',False).order('-date').fetch(10)
        
        content = []
        write = content.append
        write('<ul>')
        for post in post_list:
            write('<li><a href="%s">%s</a></li>' % ('#', post.title))
        write('</ul>')
        
        return ''.join(content)

class custom_html(object):
    """自定义HTML装饰"""
    def name(self):
        return u"自定义HTML"
    
    def body(self):
        return ''