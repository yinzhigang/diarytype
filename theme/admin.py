# -*- coding: utf-8 -*-

import web

from blog.models import Widget

from util.template import render
from util import requires_admin

class theme(object):
    """模板管理"""
    @requires_admin
    def GET(self):
        pass

class widget(object):
    """侧边条小工具"""
    @requires_admin
    def GET(self):
        widgets = Widget.all()
        
        return render('admin/widget.html',widgets=widgets)
