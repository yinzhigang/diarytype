# -*- coding: utf-8 -*-

import web

from links.models import Link
from util.template import render
from util import requires_admin

import simplejson as json

class links(object):
    """友情链接管理"""
    def GET(self):
        links = Link.all().order('sort')
        
        return render('admin/links.html', links=links)
    
    def POST(self):
        data = web.data()

        sorted_data = json.loads(data)
        for link_id, sort in sorted_data.iteritems():
            link_id = Link.get_by_id(int(link_id))
            link_id.sort = sort
            link_id.save()
        
        clear_cache()

        return json.dumps({'status': 'ok'})

class edit(object):
    """新增修改友情链接"""
    def GET(self, link_id=None):
        link = None
        if link_id:
            link = Link.get_by_id(int(link_id))
            title = u'修改友情链接'
        else:
            title = u'新增友情链接'
        
        return render('admin/link.html',link=link,title=title)
    
    def POST(self, link_id=None):
        if link_id:
            link = Link.get_by_id(int(link_id))
        else:
            link = Link()
            max_sort_link = Link.all().order('-sort').get()
            if max_sort_link:
                # max_sort_category = max_sort_category.pop()
                max_sort = max_sort_link.sort
                if not max_sort:
                    max_sort = 1
            else:
                max_sort = 0
            link.sort = max_sort + 1
        
        inp = web.input()
        link.name = inp.name
        url = inp.get('url')
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        link.url = url
        link.save()
        
        clear_cache()
        
        return web.seeother('/admin/links')

class delete(object):
    """删除友情链接"""
    def GET(self, link_id=None):
        if link_id:
            link = Link.get_by_id(int(link_id))
            link.delete()
            
            clear_cache()

        return web.seeother('/admin/links')

def clear_cache():
    """清除友情链接缓存"""
    from google.appengine.api import memcache
    memcache.delete_multi(['widget_links'])
