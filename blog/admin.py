# -*- coding: utf-8 -*-

import web

from google.appengine.api import memcache

from blog.models import Blog
from util.template import render
from util import requires_admin

class dashboard(object):
    """后台管理首页"""
    @requires_admin
    def GET(self):
        web.found('/admin/setting')

class setting(object):
    @requires_admin
    def GET(self):
        """系统设置表单"""
        import pytz
        common_timezones = pytz.common_timezones
        blog = Blog.get()
        
        return render('admin/setting.html',blog=blog,timezones=common_timezones)
    
    @requires_admin
    def POST(self):
        """保存博客信息"""
        inp = web.input()
        
        blog = Blog.get()
        blog.name = inp.name
        blog.description = inp.description
        blog.timezone = inp.timezone
        blog.custom_header = inp.custom_header
        blog.update()
        
        raise web.seeother('/admin/setting')

class habit(object):
    """习惯设置"""
    @requires_admin
    def GET(self):
        blog = Blog.get()
        return render('admin/setting_habit.html',blog=blog)
    
    @requires_admin
    def POST(self):
        inp = web.input()
        
        blog = Blog.get()
        blog.post_pagesize = int(inp.post_pagesize)
        blog.comment_pagesize = int(inp.comment_pagesize)
        blog.comment_sort = inp.comment_sort
        blog.ping_sites = inp.ping_sites
        blog.update()
        
        raise web.seeother('/admin/setting/habit')

class permalink(object):
    """固定链接设置"""
    @requires_admin
    def GET(self):
        blog = Blog.get()
        return render('admin/setting_permalink.html', blog=blog)

class install(object):
    """系统安装"""
    @requires_admin
    def GET(self):
        import pytz
        common_timezones = pytz.common_timezones
        blog = Blog.get()
        
        return render('admin/install.html',blog=blog,timezones=common_timezones)
    
    @requires_admin
    def POST(self):
        import os, datetime, yaml
        
        from blog import widgets as blog_widgets
        from blog.models import Widget
        from theme.models import Theme, ThemeFile
        
        from settings import VERSION, THEME_TEMPLATE_DIR
        
        widgets = Widget.all()
        for widget in widgets:
            widget.delete()
        
        widget_modules = blog_widgets.default_widgets
        for widget_name in widget_modules:
            widget = Widget(key_name=widget_name)
            widget.name = widget_name
            widget.package = 'blog.widgets.%s' % widget_name
            widget.save()
        
        inp = web.input()
        blog = Blog.get()
        blog.name = inp.name
        blog.description = inp.description
        blog.timezone = inp.timezone
        blog.theme_widget = '{"1":[{"name":"categories"},{"name":"hot_tags"},{"name":"recent_entries"},{"name":"recent_comments"},{"name":"links"}]}'
        blog.version = VERSION
        blog.update()
        
        default_theme = os.path.join(THEME_TEMPLATE_DIR, 'default')
        config = open(os.path.join(default_theme, 'config.yaml')).read()
        config = yaml.load(config)
        
        theme_name = config.get("name")
        theme = Theme.get_by_key_name(theme_name)
        if not theme:
            theme = Theme(key_name=theme_name)
        theme.name = config.get("name")
        theme.author = config.get("author")
        theme.homepage = config.get("homepage")
        theme.description = config.get("description")
        theme.sidebar = config.get("sidebar")
        screenshot = open(os.path.join(default_theme, 'screenshot.png')).read()
        theme.screenshot = screenshot
        theme.save()
        
        for root, dirs, files in os.walk(default_theme, True):
            path = root.replace(default_theme, '')
            if path.startswith('/'):
                path = path[1:]
            for filename in files:
                f = os.path.join(path, filename)
                if filename in ['config.yaml', 'screenshot.png']:
                    continue
                
                theme_file = ThemeFile.all().filter('theme_name =', theme_name).\
                        filter('filename =', f).get()
                if not theme_file:
                    theme_file = ThemeFile()
                    theme_file.theme_name = theme_name
                    theme_file.filename = f
                theme_file.filecontent = open(os.path.join(default_theme, f)).read()
                if f.endswith('.html'):
                    filetype = 'template'
                else:
                    filetype = 'file'
                theme_file.filetype = filetype
                theme_file.modified = datetime.datetime.now()
                theme_file.save()
        
        raise web.seeother('/admin')

class warmup(object):
    """供 Appengine 内部调用"""
    def GET(self):
        pass
        
class clear_cache(object):
    """清除memcache缓存"""
    @requires_admin
    def GET(self):
        memcache.flush_all()
        import jinja2
        jinja2.clear_caches()
        
        raise web.seeother('/admin/setting')
