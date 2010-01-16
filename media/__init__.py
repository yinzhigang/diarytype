# -*- coding: utf-8 -*-

import web

import binascii
import time
import email
import mimetypes

from google.appengine.ext import blobstore

from media.models import Media

class media_thumb(object):
    """媒体文件浏览"""
    def GET(self, thumb, blob_key):
        if blob_key.isdigit():
            media = Media.get_by_id(int(blob_key))
        else:
            media = Media.all().filter('blobstore_key =', blob_key).get()
        if not media:
            raise web.notfound()
        
        mime_type, encoding = mimetypes.guess_type(media.name)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        if thumb == 'small':
            body = str(media.small)
        else:
            body = str(media.big)
        
        etag = str(binascii.crc32(body))
        SetCacheHeader(etag)
        
        match = web.ctx.env.get('HTTP_IF_NONE_MATCH')
        if match and match == etag:
            raise web.notmodified()
        
        web.header('Content-Type', mime_type)
        return body

class media_source(object):
    def GET(self, blob_key):
        if blob_key.isdigit():
            media = Media.get_by_id(int(blob_key))
            if not media:
                raise web.notfound()
            mime_type, encoding = mimetypes.guess_type(media.name)
            if not mime_type:
                mime_type = 'application/octet-stream'
            body = str(media.source)
            
            etag = str(binascii.crc32(body))
            SetCacheHeader(etag)
            
            match = web.ctx.env.get('HTTP_IF_NONE_MATCH')
            if match and match == etag:
                raise web.notmodified()
            
            web.header('Content-Type', mime_type)
            return body
        else:
            blob_info = blobstore.get(blob_key)
            if not blob_info:
                raise web.notfound()
            web.header('Content-Type', blob_info.content_type)
            web.header(blobstore.BLOB_KEY_HEADER, blob_key)

            

MAX_AGE = 86400
def SetCacheHeader(etag=None):
    """缓存控制"""
    web.header('Expires', email.Utils.formatdate(
                        time.time() + MAX_AGE, usegmt=True))
    web.header('Cache-Control', 'public, max-age=%d' % MAX_AGE)
    if etag:
        web.header('ETag', etag)
