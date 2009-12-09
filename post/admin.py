# -*- coding: utf-8 -*-

import web

from post.models import Post, Tag
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

class post(object):
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
        
        return render('admin/post.html',post=post,title=title)
    
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
