# -*- coding: utf-8 -*-

from google.appengine.ext import db
from post.models import Post

class Comment(db.Model):
    """评论模块"""
    post = db.ReferenceProperty(Post)
    name = db.StringProperty()
    email = db.EmailProperty()
    homepage = db.LinkProperty()
    content = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
