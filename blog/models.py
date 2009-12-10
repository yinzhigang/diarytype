# -*- coding: utf-8 -*-

from google.appengine.ext import db

cache = {}
class Blog(db.Model):
    """博客基本信息"""
    name = db.StringProperty(multiline=False,default='')
    description = db.TextProperty(default='')
    enable_xmlrpc = db.BooleanProperty(default=False)
    owner = db.StringProperty(multiline=False,default='admin')
    theme = db.StringProperty(multiline=False,default='default')
    custom_header = db.TextProperty(default='')
    
    @classmethod
    def get(cls):
        """获取博客信息，此模型只有一条记录"""
        blog = cache.get('blog')
        if not blog:
            blog = cls.get_by_key_name('blog')
            if not blog:
                blog = cls(key_name='blog')
                blog.save()
            cache['blog'] = blog
        return blog
    
