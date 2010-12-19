# -*- coding: utf-8 -*-

import web
from datetime import datetime

from blog.models import Blog, blog
from post.models import Post, Tag
from category.models import Category
from util.template import render
from util import requires_admin
# from util.pager import PagerQuery
from util.pager import Pager

class posts(object):
    """日志列表处理"""
    @requires_admin
    def GET(self):
        inp = web.input()
        page = inp.get('page')
        if not page:
            page = 1
        # offset = (page - 1) * 10
        # bookmark = inp.get('bookmark')
        
        # query = PagerQuery(Post).order('-date')
        # prev, posts, next = query.fetch(10, bookmark)
        # posts = Post.all().order('-date')
        pager = Pager(Post, 10).order('-date')
        posts = pager.fetch(page)
        # posts = Post.all().order('-date').fetch(10, offset)
        # count = Post.all().count()
        
        return render('admin/posts.html',posts=posts,pager=pager)#prev=prev,next=next)

class edit(object):
    """日志新增修改"""
    @requires_admin
    def GET(self, post_id=None):
        post = {}
        if post_id:
            # post = Post.get(db.Key.from_path(Post.kind(), int(post_id)))
            post = Post.get_by_id(int(post_id))
            title = u'修改日志'
        else:
            title = u'写新日志'
            post['date'] = datetime.now()
        
        categories = Category.all().order('sort')
        
        return render('admin/post.html',
                      post=post,
                      title=title,
                      categories=categories)
    
    @requires_admin
    def POST(self, post_id=None):
        """保存日志信息"""
        import pytz
        
        if post_id:
            post = Post.get_by_id(int(post_id))
        else:
            post = Post()
        
        inp = web.input()
        
        post.title = inp.title
        post.alias = inp.alias
        post.content = inp.content
        post.excerpt = inp.excerpt
        if inp.get('date'):
            tz = pytz.timezone(blog.timezone)
            date = inp.get('date')
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            date_tz = date.replace(tzinfo=tz)
            # datetime = time.mktime(date)
            post.date = date_tz
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
        
        clear_cache()
        
        from google.appengine.api.labs import taskqueue
        queue = taskqueue.Queue()
        url = '/task/ping_sites'
        ping_task = taskqueue.Task(countdown=5, url=url)
        queue.add(ping_task)
        
        raise web.seeother('/admin/posts')

class delete(object):
    """删除日志"""
    @requires_admin
    def GET(self, post_id):
        if post_id:
            post = Post.get_by_id(int(post_id))
            post.delete()
            
            clear_cache()
        
        raise web.seeother('/admin/posts')

def clear_cache():
    """清除分类缓存"""
    from google.appengine.api import memcache
    memcache.delete_multi(['widget_post_list', 'widget_tag_list',
                           'widget_category_list'])

class ping_sites(object):
    """更新通知"""
    def GET(self):
        import xmlrpclib
        import logging
        if blog.ping_sites:
            sites = blog.ping_sites.split('\n')
            for site in sites:
                site = site.strip()
                logging.info(site)
                name = blog.name
                home = web.ctx.home
                feed = web.ctx.home + '/feed'
                xmlrpc = xmlrpclib.Server(site)
                try:
                    s = xmlrpc.weblogUpdates.extendedPing(name, home, feed)
                    logging.info(s)
                except:
                    logging.info('not ext ping')
                    try:
                        s = xmlrpc.weblogUpdates.ping(name, home)
                        logging.info(s)
                    except:
                        logging.info('except')
        
        return 'ok'
    
    def POST(self):
        return self.GET()
