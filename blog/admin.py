# -*- coding: utf-8 -*-

import web

from blog.models import Blog
from util.template import render
from util import requires_admin

class setting:
    @requires_admin
    def GET(self):
        """系统设置表单"""
        blog = Blog.get()
        
        return render('admin/setting.html',blog=blog)
    
    @requires_admin
    def POST(self):
        """保存博客信息"""
        inp = web.input()
        
        blog = Blog.get()
        blog.name = inp.name
        blog.description = inp.description
        blog.save()
        
        raise web.seeother('/admin/setting')
