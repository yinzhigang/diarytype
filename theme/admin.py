# -*- coding: utf-8 -*-

import web

from util.template import render
from util import requires_admin

class theme(object):
    """模板管理"""
    def GET(self):
        pass

class widget(object):
    """侧边条小工具"""
    def GET(self):
        
        return render('admin/widget.html')
