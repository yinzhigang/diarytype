# -*- coding: utf-8 -*-

import web

from blog.base_front import BaseFront

from post.models import Post, Tag
from category.models import Category
from util.template import render
from util.pager import PagerQuery

class posts(BaseFront):
    """首页文章列表"""
    def GET(self):
        inp = web.input()
        bookmark = inp.get('bookmark')
        
        query = PagerQuery(Post).filter('hidden =',False).order('-date')
        prev, posts, next = query.fetch(10, bookmark)
        
        return render('theme/index.html',posts=posts,prev=prev,next=next)

class category_post(BaseFront):
    """显示分类文章"""
    def GET(self, category_name):
        if category_name.isdigit():
            category = Category.get_by_id(int(category_name))
        else:
            category = Category.all().filter('alias =', category_name).get()
        
        inp = web.input()
        bookmark = inp.get('bookmark')
            
        query = PagerQuery(Post).filter('hidden =', False)
        query.filter('category =', category)
        query.order('-date')
        prev, posts, next = query.fetch(10, bookmark)
        
        return render('theme/index.html',posts=posts,prev=prev,next=next)

class show(BaseFront):
    """显示单篇日志"""
    def GET(self, post_id):
        post = Post.get_by_id(int(post_id))
        
        return render('theme/show.html',post=post)
