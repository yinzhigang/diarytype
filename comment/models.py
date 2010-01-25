# -*- coding: utf-8 -*-

from google.appengine.ext import db
from post.models import Post

from jinja2.utils import escape
import logging

class Comment(db.Model):
    """评论模块"""
    post = db.ReferenceProperty(Post)
    name = db.StringProperty()
    email = db.StringProperty(default='')
    homepage = db.StringProperty(default='')
    content = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    def __getattribute__(self, name):
        logging.info(name)
        ret = object.__getattribute__(self, name)
        if name in ['name', 'email', 'homepage', 'content']:
            ret = escape(ret)
        
        return ret
