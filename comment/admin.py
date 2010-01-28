# -*- coding: utf-8 -*-

import web

from comment.models import Comment
from util.template import render
from util import requires_admin
from util.pager import PagerQuery

class comments(object):
    """评论管理"""
    @requires_admin
    def GET(self):
        inp = web.input()
        bookmark = inp.get('bookmark')
        
        query = PagerQuery(Comment).order('-created')
        prev, comments, next = query.fetch(10, bookmark)
        
        return render('admin/comments.html',
                      comments=comments,prev=prev,next=next)

class delete(object):
    """删除选中评论"""
    @requires_admin
    def GET(self, comment_id = None):
        if comment_id:
            comment = Comment.get_by_id(int(comment_id))
            comment.delete()
            clear_cache()

        return web.seeother('/admin/comments')

def clear_cache():
    """清除友情链接缓存"""
    from google.appengine.api import memcache
    memcache.delete_multi(['widget_comments'])
