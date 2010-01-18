# -*- coding: utf-8 -*-

import web

from google.appengine.ext import blobstore
from google.appengine.api import images

from media.models import Media

from util.template import render
from util import requires_admin

import logging

class media_list(object):
    """媒体管理"""
    @requires_admin
    def GET(self):
        media_list = Media.all().order('-created')
        
        return render('admin/media.html',media_list=media_list)

class upload(object):
    """媒体上传"""
    @requires_admin
    def GET(self):
        try:
            upload_url = blobstore.create_upload_url('/admin/media/upload')
        except:
            upload_url = '/admin/media/upload'
        
        return render('admin/media_upload_blobstore.html',
                      upload_url=upload_url)
    
    @requires_admin
    def POST(self):
        import cgi
        fields = cgi.FieldStorage()
        file_fields = fields['media']
        if not isinstance(file_fields, list):
            file_fields = [file_fields]
        
        for field in file_fields:
            media = Media()
            try:
                blob_info = blobstore.parse_blob_info(field)
                key = str(blob_info.key())
                
                small_img = images.Image(blob_key=key)
                big_img = images.Image(blob_key=key)
                media.name = blob_info.filename.decode('utf-8')
                media.blobstore_key = key
            except:
                source = field.value
                media.name = field.filename.decode('utf-8')
                media.source = source
                small_img = images.Image(source)
                big_img = images.Image(source)
            
            small_img.resize(width=200, height=150)
            small_img.im_feeling_lucky()
            small_thumb = small_img.execute_transforms(output_encoding=images.JPEG)
            
            big_img.resize(width=650, height=1000)
            big_img.im_feeling_lucky()
            big_thumb = big_img.execute_transforms(output_encoding=images.JPEG)
            
            media.small = small_thumb
            media.big = big_thumb
            media.save()
        
        raise web.seeother('/admin/media')

class delete(object):
    @requires_admin
    def GET(self, blob_key):
        if blob_key.isdigit():
            media = Media.get_by_id(int(blob_key))
        else:
            media = Media.all().filter('blobstore_key =', blob_key).get()
            blob_info = blobstore.get(blob_key)
            blob_info.delete()
        if not media:
            raise web.notfound()
        
        media.delete()
        
        raise web.seeother('/admin/media')
