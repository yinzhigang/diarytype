# -*- coding: utf-8 -*-

import web

from comment.models import Comment
from util.template import render
from util import requires_admin
from util.pager import PagerQuery

class comments(object):
    """评论管理"""
    def GET(self):
        inp = web.input()
        bookmark = inp.get('bookmark')
        
        query = PagerQuery(Comment).order('-created')
        prev, comments, next = query.fetch(10, bookmark)
        
        return render('admin/comments.html',
                      comments=comments,prev=prev,next=next)
