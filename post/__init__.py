# -*- coding: utf-8 -*-

import web

from blog.base_front import BaseFront

from post.models import Post, Tag
from category.models import Category
from comment.models import Comment
from util.template import render
from util.pager import PagerQuery

PAGE_SIZE = 10

class posts(BaseFront):
    """首页文章列表"""
    def GET(self):
        inp = web.input()
        bookmark = inp.get('bookmark')
        
        query = PagerQuery(Post).filter('hidden =',False).order('-date')
        prev, posts, next = query.fetch(PAGE_SIZE, bookmark)
        
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
        prev, posts, next = query.fetch(PAGE_SIZE, bookmark)
        
        return render('theme/index.html',posts=posts,prev=prev,next=next)

class tag_post(BaseFront):
    """显示Tag文章列表"""
    def GET(self, tag_name):
        # tag = Tag.all().filter('name =', tag_name).get()
        
        inp = web.input()
        bookmark = inp.get('bookmark')
        
        query = PagerQuery(Post).filter('hidden =', False)
        query.filter('tags =', tag_name)
        query.order('-date')
        prev, posts, next = query.fetch(PAGE_SIZE, bookmark)
        
        return render('theme/index.html',posts=posts,prev=prev,next=next)

class show(BaseFront):
    """显示单篇日志"""
    def GET(self, post_id):
        import hashlib
        post = Post.get_by_id(int(post_id))
        if not post:
            raise web.notfound()
        
        fullpath = web.ctx.home + web.ctx.fullpath
        check = "%s%s" % (fullpath, post.key())
        checksum = hashlib.sha1(check).hexdigest()
        
        comments = Comment.all().filter('post =', post).order('-created').fetch(10)
        
        return render('theme/show.html',post=post,checksum=checksum,comments=comments)
