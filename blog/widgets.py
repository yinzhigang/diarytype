# -*- coding: utf-8 -*-

from StringIO import StringIO

from post.models import Post
from category.models import Category

class Widget(object):
    """装饰"""
    params = None
    def __init__(self, params=None):
        self.params = params

class categories(Widget):
    """文章分类装饰"""
    def name(self):
        return u"文章分类"
    
    def widget(self):
        category_list = Category.all().order('sort')
        
        for category in category_list:
            pass
        return category_list

def recent_entries(params=None):
    """最新文章"""
    pass