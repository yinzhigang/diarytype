# -*- coding: utf-8 -*-

import os
import web

import binascii
import time
import email
import mimetypes
from settings import THEME_TEMPLATE_DIR

from theme.models import ThemeFile

from google.appengine.api import memcache

class theme_file(object):
    """模板文件处理"""
    def GET(self, theme, filename):
        mime_type, encoding = mimetypes.guess_type(filename)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        theme_file_query = ThemeFile.all().filter('theme_name =', theme)
        theme_file_query.filter('filename =', filename)
        theme_file_query.filter('filetype =', 'file')
        f = theme_file_query.get()
        
        if not theme_file:
            raise web.notfound()
        
        body = str(f.filecontent)
        etag = str(binascii.crc32(body))
        self.SetCacheHeader(etag)
        
        match = web.ctx.env.get('HTTP_IF_NONE_MATCH')
        if match and match == etag:
            raise web.notmodified()
        web.header('Content-Type', mime_type)
        return body
        # theme_path = os.path.join(THEME_TEMPLATE_DIR, theme)
        # if os.path.isdir(theme_path):
        #     try:
        #         filename = os.path.join(theme_path, filename)
        #         f = open(filename, 'rb')
        #         body = f.read()
        #         f.close()
        #         etag = str(binascii.crc32(body))
        #         self.SetCacheHeader(etag)
        #         
        #         match = web.ctx.env.get('HTTP_IF_NONE_MATCH')
        #         if match and match == etag:
        #             raise web.notmodified()
        #     except IOError:
        #         body = None
        # else:
        #     body = None
        
        # if not body:
        #     raise web.notfound()
    
    MAX_AGE = 86400
    
    def SetCacheHeader(self, etag=None):
        """缓存控制"""
        web.header('Expires', email.Utils.formatdate(
            time.time() + self.MAX_AGE, usegmt=True))
        web.header('Cache-Control', 'public, max-age=%d' % self.MAX_AGE)
        web.header('ETag', etag)
