# -*- coding: utf-8 -*-

import web

import blog.widgets
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

class init_widget(object):
    """初始化默认装饰"""
    @requires_admin
    def GET(self):
        widgets = Widget.all()
        for widget in widgets:
            widget.delete()
        
        widget_modules = blog.widgets.default_widgets
        for widget_name in widget_modules:
            widget = Widget(key_name=widget_name)
            widget.name = widget_name
            widget.package = 'blog.widgets.%s' % widget_name
            widget.save()
        
        raise web.seeother('/admin/theme/widget')

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
                     )
    
    @requires_admin
    def POST(self):
        """保存模板装饰布局"""
        data = web.data()
        blog = Blog.get()
        blog.theme_widget = data
        blog.update()
        
        return json.dumps({'status': 'ok'})
