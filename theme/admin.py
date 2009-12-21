# -*- coding: utf-8 -*-

import web

from blog.models import Blog, Widget

from util.template import render
from util import requires_admin

from blog.base_front import Processor
import simplejson as json

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
        
        blog = Blog.get()
        theme = blog.theme
        
        processor = Processor()
        sidebar_num = 1
        
        # return theme_widget.get('1')
        return render('admin/widget.html',
                      widgets=widgets,
                      sidebar_num=sidebar_num,
                      processor=processor
                      # theme_widget=theme_widget
                     )
    
    @requires_admin
    def POST(self):
        """保存模板装饰布局"""
        data = web.data()
        blog = Blog.get()
        blog.theme_widget = data
        blog.update()
        
        return json.dumps({'status': 'ok'})
