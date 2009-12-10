# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Category(db.Model):
    """分类"""
    name = db.StringProperty(default='')
    count = db.IntegerProperty(default=0)
    sort = db.IntegerProperty()
