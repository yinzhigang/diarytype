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
    theme_widget = db.TextProperty(default='')
    
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
    
    def update(self):
        """更新博客信息并清除缓存"""
        cache['blog'] = self
        self.save()

class Widget(db.Model):
    """侧边条工具"""
    name = db.StringProperty(multiline=False)
    package = db.StringProperty()
    
    def item(self, params=None):
        """获取装饰控制对象"""
        x = self.package.split('.')
        mod, cls = '.'.join(x[:-1]), x[-1]
        mod = __import__(mod, globals(), locals(), [""])
        cls = getattr(mod, cls)
        item = cls(params)
        return item
