# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Media(db.Model):
    """媒体文件"""
    name = db.StringProperty()
    filetype = db.StringProperty()
    small = db.BlobProperty()
    big = db.BlobProperty()
    created = db.DateTimeProperty(auto_now_add=True)
