# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Theme(db.Model):
    """模板存储"""
    name = db.StringProperty()
    description = db.TextProperty()
    author = db.StringProperty()
    homepage = db.StringProperty()
    config = db.TextProperty()
    screenshot = db.BlobProperty()
    sidebar = db.IntegerProperty(default=1)

class ThemeFile(db.Model):
    """模板文件"""
    # theme = db.ReferenceProperty(Theme)
    theme_name = db.StringProperty()
    filename = db.StringProperty(multiline=False)
    filetype = db.StringProperty(choices=['template', 'file'])
    filecontent = db.BlobProperty()
    modified = db.DateTimeProperty()
