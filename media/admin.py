# -*- coding: utf-8 -*-

import web

from google.appengine.ext import blobstore
from media.models import Media

class media_list(object):
    """媒体管理"""
    def GET(self):
        media_list = Media.all().order('-created')
        pass

class upload(object):
    """媒体上传"""
    def GET(self):
        pass
    
    def POST(self):
        pass
