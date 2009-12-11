# -*- coding: utf-8 -*-

import web

from comment.models import Comment

class comment(object):
    """发布评论"""
    def POST(self):
        inp = web.input()
        
        username = inp.get('username')
        