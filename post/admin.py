# -*- coding: utf-8 -*-

import web

from post.models import Post, Tag
from category.models import Category
from util.template import render
from util import requires_admin
from util.pager import PagerQuery

class posts(object):
    """日志列表处理"""
    @requires_admin
    def GET(self):
        inp = web.input()
        bookmark = inp.get('bookmark')
        
        query = PagerQuery(Post).order('-date')
        prev, posts, next = query.fetch(10, bookmark)
        # posts = Post.all().order('-date')
        
        return render('admin/posts.html',posts=posts,prev=prev,next=next)

class edit(object):
    """日志新增修改"""
    @requires_admin
    def GET(self, post_id=None):
        post = None
        if post_id:
            # post = Post.get(db.Key.from_path(Post.kind(), int(post_id)))
            post = Post.get_by_id(int(post_id))
            title = u'修改日志'
        else:
            title = u'写新日志'
        
        categories = Category.all().order('sort')
        
        return render('admin/post.html',
                      post=post,
                      title=title,
                      categories=categories)
    
    @requires_admin
    def POST(self, post_id=None):
        """保存日志信息"""
        if post_id:
            post = Post.get_by_id(int(post_id))
        else:
            post = Post()
        
        inp = web.input()
        
        post.title = inp.title
        post.content = inp.content
        post.excerpt = inp.excerpt
        post.allow_comment = bool(inp.get('allow_comment'))
        post.allow_ping = bool(inp.get('allow_ping'))
        post.hidden = bool(inp.get('hidden'))
        
        # 以下分类代码写的比较乱
        # 文章添加分类最简单，直接分类统计加1
        # 分类修改则取得原分类减1，新分类加1
        # 删除分类则将旧分类减1
        category_key = inp.get('category')
        if category_key:
            category = Category.get(category_key)
        if post.category:
            if unicode(post.category.key()) != unicode(category_key):
                post.category.count = post.category.count - 1
                post.category.save()
                if category_key:
                    post.category = category
                    category.count = category.count + 1
                    category.save()
                else:
                    post.category = None
        elif category_key:
            post.category = category
            category.count = category.count + 1
            category.save()
        
        tags = inp.tags
        if tags:
            tags = tags.split(',')
            post.tags = tags
            for tag in tags:
                Tag.add(tag)
        post.save()
        
        raise web.seeother('/admin/posts')

class delete(object):
    """删除日志"""
    @requires_admin
    def GET(self, post_id):
        if post_id:
            post = Post.get_by_id(int(post_id))
            post.delete()
        
        raise web.seeother('/admin/posts')
