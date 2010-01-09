# -*- coding: utf-8 -*-

import web

import blog.widgets
from blog.models import Blog, Widget, blog
from theme.models import Theme, ThemeFile

from util.template import render
from util import requires_admin

from blog.base_front import Processor
import simplejson as json
import yaml

class theme(object):
    """模板管理"""
    @requires_admin
    def GET(self):
        use_theme = blog.theme
        themes = Theme.all()
        
        return render('admin/theme.html',themes=themes,use_theme=use_theme)
    
    @requires_admin
    def import_theme(self):
        import os
        import zipfile
        import datetime
        from settings import THEME_TEMPLATE_DIR
        
        zip_filename = os.path.join(THEME_TEMPLATE_DIR, 'RewindCity.zip')
        fileinfo = zipfile.ZipFile(zip_filename)
        
        config = yaml.load(fileinfo.read('config.yaml'))
        
        theme_name = config.get("name")
        default_theme = Theme.get_by_key_name(theme_name)
        if not default_theme:
            default_theme = Theme(key_name=theme_name)
        default_theme.name = config.get("name")
        default_theme.author = config.get("author")
        default_theme.homepage = config.get("homepage")
        default_theme.description = config.get("description")
        default_theme.sidebar = config.get("sidebar")
        screenshot = fileinfo.read('screenshot.png')
        default_theme.screenshot = screenshot
        default_theme.save()
                
        for i in fileinfo.infolist():
            filename = i.filename
            if filename.endswith('/') or \
                    filename in ['config.yaml', 'screenshot.png']:
                continue
            
            file_size = i.file_size
            date_time = i.date_time
            date_time = datetime.datetime(*date_time)
            theme_file = ThemeFile.all().filter('theme_name =', theme_name).\
                    filter('filename =', filename).get()
            if not theme_file:
                theme_file = ThemeFile()
                theme_file.theme_name = theme_name
                theme_file.filename = filename
            theme_file.filecontent = fileinfo.read(filename)
            if filename.endswith('.html'):
                filetype = 'template'
            else:
                filetype = 'file'
            theme_file.filetype = filetype
            theme_file.modified = date_time
            theme_file.save()
        
        return config

class theme_screenshot(object):
    """模板缩略图"""
    @requires_admin
    def GET(self, name):
        theme = Theme.get_by_key_name(name)
        screenshot = str(theme.screenshot)
        
        web.header('Content-Type', 'image/png')
        return screenshot

class change_theme(object):
    """修改当前使用模板"""
    @requires_admin
    def GET(self, name):
        from util.template import env
        blog.theme = name
        blog.update()
        
        env.cache.clear()
        raise web.seeother('/admin/theme')

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
        theme = blog.theme
        
        processor = Processor()
        theme = Theme.get_by_key_name(theme)
        sidebar_num = theme.sidebar
        
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
