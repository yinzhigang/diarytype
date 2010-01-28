# -*- coding: utf-8 -*-

import web
import hashlib

from post.models import Post
from comment.models import Comment

class comment(object):
    """发布评论"""
    def POST(self):
        inp = web.input()
        
        post_key = inp.get('post')
        post = Post.get(post_key)
        if not post or not post.allow_comment:
            raise web.forbidden()
        
        checksum = inp.get('checksum')
        referer = web.ctx.env.get('HTTP_REFERER')
        i = referer.find('#')
        if i > 0:
            referer = referer[:i]
        
        real_checksum = hashlib.sha1(referer + post_key).hexdigest()
        real_checksum = real_checksum[:15] + 'l' + real_checksum[16:]
        if checksum != real_checksum:
            raise web.forbidden()
        
        name = inp.get('name')
        email = inp.get('email')
        homepage = inp.get('homepage')
        if not homepage.startswith('http://') and \
                            not homepage.startswith('https://'):
            homepage = 'http://' + homepage
            
        content = inp.get('content')
        
        comment = Comment()
        comment.post = post
        comment.name = name
        comment.email = email
        comment.homepage = homepage
        comment.content = content
        comment.save()

        clear_cache()
        
        post.comment_count = post.comment_count + 1
        post.save()
        
        raise web.seeother(referer + '#cmt')

def clear_cache():
    """清除友情链接缓存"""
    from google.appengine.api import memcache
    memcache.delete_multi(['widget_comments'])
