# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Category(db.Model):
    """分类"""
    name = db.StringProperty(default='')
    alias = db.StringProperty(default='')
    count = db.IntegerProperty(default=0)
    sort = db.IntegerProperty()
    
    def getUrl(self):
        if self.alias:
            return '/category/%s' % self.alias
        else:
            return '/category/%s' % self.key().id()
