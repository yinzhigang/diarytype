# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Link(db.Model):
    name = db.StringProperty()
    url = db.StringProperty()
    sort = db.IntegerProperty()
