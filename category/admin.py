# -*- coding: utf-8 -*-

import web

from category.models import Category
from util.template import render
from util import requires_admin

import simplejson as json

class categories(object):
    """分类管理"""
    @requires_admin
    def GET(self):
        categories = Category.all().order('sort')
        
        return render('admin/categories.html',categories=categories)
    
    def POST(self):
        data = web.data()
        
        sorted_data = json.loads(data)
        for category_id, sort in sorted_data.iteritems():
            category = Category.get_by_id(int(category_id))
            category.sort = sort
            category.save()
        
        return json.dumps({'status': 'ok'})

class edit(object):
    """分类新增修改"""
    def GET(self, category_id=None):
        category = None
        if category_id:
            category = Category.get_by_id(int(category_id))
            title = u'修改分类'
        else:
            title = u'新增分类'
        
        return render('admin/category.html',category=category,title=title)
    
    def POST(self, category_id=None):
        if category_id:
            category = Category.get_by_id(int(category_id))
        else:
            category = Category()
            max_sort_category = Category.all().order('-sort').get()
            if max_sort_category:
                # max_sort_category = max_sort_category.pop()
                max_sort = max_sort_category.sort
                if not max_sort:
                    max_sort = 0
            else:
                max_sort = 0
            category.sort = max_sort + 1
        
        inp = web.input()
        category.name = inp.name
        category.alias = inp.get('alias')
        category.save()
        
        return web.seeother('/admin/categories')

class delete(object):
    """删除分类"""
    def GET(self, category_id=None):
        if category_id:
            category = Category.get_by_id(int(category_id))
            category.delete()
        
        return web.seeother('/admin/categories')
