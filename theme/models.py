# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Theme(db.Model):
    """模板存储"""
    name = db.StringProperty()
    description = db.TextProperty()
    config = db.TextProperty()
    screenshot = db.BlobProperty()
    author = db.StringProperty()

class ThemeFile(db.Model):
    """模板文件"""
    theme = db.ReferenceProperty(Theme)
    filename = db.StringProperty(multiline=False)
    filetype = db.StringProperty(choices=['template', 'file'])
    filecontent = db.BlobProperty()
    created = db.DateTimeProperty(auto_now=True)
