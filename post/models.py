# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2009

@author: sxin
'''

from google.appengine.ext import db

class Post(db.Model):
    """文章存储结构"""
    title = db.StringProperty()
    content = db.TextProperty()
    tags = db.StringListProperty()
    excerpt = db.TextProperty()
    # status = db.StringProperty(multiline=False,default='1',choices=[
    #         '0','1'])
    
    hidden = db.BooleanProperty(default=False)
    allow_comment = db.BooleanProperty(default=True)
    allow_ping = db.BooleanProperty(default=True)
    date = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def taglist(self):
        """获取Tag字符"""
        try:
            return ','.join(self.tags)
        except:
            return ''

class Tag(db.Model):
    """Tag Model"""
    name = db.StringProperty()
    count = db.IntegerProperty(default=0)
    
    @classmethod
    def add(cls, name):
        """新增Tag"""
        if name:
            tag= Tag.get_by_key_name(name)
            if not tag:
                tag=Tag(key_name=name)
                tag.name = name

            tag.count += 1
            tag.save()
            return tag
        else:
            return None
