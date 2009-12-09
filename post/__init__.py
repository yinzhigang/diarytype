# -*- coding: utf-8 -*-

import web

from post.models import Post
from util.template import render

class posts(object):
    """首页文章列表"""
    def GET(self):
        posts = Post.all().filter('hidden =',False).order('-date')
        
        return render('theme/index.html',posts=posts)

class show(object):
    """显示单篇日志"""
    def GET(self, post_id):
        post = Post.get_by_id(int(post_id))
        
        return render('theme/show.html',post=post)
        