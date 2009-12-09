# -*- coding: utf-8 -*-

import web

from post.models import Post
from util.template import render
from util.pager import PagerQuery

class posts(object):
    """首页文章列表"""
    def GET(self):
        inp = web.input()
        bookmark = inp.get('bookmark')
        
        query = PagerQuery(Post).filter('hidden =',False).order('-date')
        prev, posts, next = query.fetch(10, bookmark)
        # posts = Post.all().filter('hidden =',False).order('-date')
        
        return render('theme/index.html',posts=posts,prev=prev,next=next)

class show(object):
    """显示单篇日志"""
    def GET(self, post_id):
        post = Post.get_by_id(int(post_id))
        
        return render('theme/show.html',post=post)
        