# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Media(db.Model):
    """媒体文件"""
    name = db.StringProperty()
    blobstore_key = db.StringProperty()
    filetype = db.StringProperty(default="image")
    small = db.BlobProperty()
    big = db.BlobProperty()
    source = db.BlobProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
    def getSourceUrl(self):
        file_ext = self.name.split('.').pop().lower()
        if self.blobstore_key:
            key = self.blobstore_key
        else:
            key = self.key().id()
        return '/media/source/%s.%s' % (key, file_ext)
    
    def getSmallUrl(self):
        file_ext = self.name.split('.').pop().lower()
        if self.blobstore_key:
            key = self.blobstore_key
        else:
            key = self.key().id()
        return '/media/small/%s.%s' % (key, file_ext)
    
    def getBigUrl(self):
        file_ext = self.name.split('.').pop().lower()
        if self.blobstore_key:
            key = self.blobstore_key
        else:
            key = self.key().id()
        return '/media/big/%s.%s' % (key, file_ext)
