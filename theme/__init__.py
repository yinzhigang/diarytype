# -*- coding: utf-8 -*-

import os
import web

import mimetypes
from settings import THEME_TEMPLATE_DIR

class theme_file(object):
    """模板文件处理"""
    def GET(self, theme, filename):
        mime_type, encoding = mimetypes.guess_type(filename)
        if not mime_type:
            mime_type = 'application/octet-stream'
        theme_path = os.path.join(THEME_TEMPLATE_DIR, theme)
        if os.path.isdir(theme_path):
            try:
                filename = os.path.join(theme_path, filename)
                f = open(filename, 'rb')
                body = f.read()
                f.close()
            except IOError:
                body = None
        else:
            body = None
        
        if not body:
            raise web.notfound()
        else:
            web.header('Content-Type', mime_type)
            return body
