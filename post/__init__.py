# -*- coding: utf-8 -*-

import web

from blog.base_front import BaseFront

from blog.models import Blog, blog
from post.models import Post, Tag
from category.models import Category
from comment.models import Comment

from util.template import render
# from util.pager import PagerQuery
from util.pager import Pager

PAGE_SIZE = 10

class posts(BaseFront):
    """首页文章列表"""
    def GET(self):
        inp = web.input()
        # bookmark = inp.get('bookmark')
        # 
        # query = PagerQuery(Post).filter('hidden =',False).order('-date')
        # prev, posts, next = query.fetch(blog.post_pagesize, bookmark)
        page = inp.get('page')
        if not page:
            page = 1
        pager = Pager(Post, blog.post_pagesize).order('-date')
        pager.filter('hidden =', False)
        posts = pager.fetch(page)
        
        return render('theme/index.html',posts=posts,pager=pager)#prev=prev,next=next)

class category_post(BaseFront):
    """显示分类文章"""
    def GET(self, category_name):
        if category_name.isdigit():
            category = Category.get_by_id(int(category_name))
        else:
            category = Category.all().filter('alias =', category_name).get()
        
        inp = web.input()
        # bookmark = inp.get('bookmark')
        # 
        # query = PagerQuery(Post).filter('hidden =', False)
        # query.filter('category =', category)
        # query.order('-date')
        # prev, posts, next = query.fetch(blog.post_pagesize, bookmark)
        page = inp.get('page')
        if not page:
            page = 1
        pager = Pager(Post, blog.post_pagesize).order('-date')
        pager.filter('hidden =', False)
        pager.filter('category =', category)
        posts = pager.fetch(page)
        
        return render('theme/index.html',posts=posts,pager=pager)#prev=prev,next=next)

class tag_post(BaseFront):
    """显示Tag文章列表"""
    def GET(self, tag_name):
        # tag = Tag.all().filter('name =', tag_name).get()
        
        inp = web.input()
        # bookmark = inp.get('bookmark')
        # 
        # query = PagerQuery(Post).filter('hidden =', False)
        # query.filter('tags =', tag_name)
        # query.order('-date')
        # prev, posts, next = query.fetch(blog.post_pagesize, bookmark)
        page = inp.get('page')
        if not page:
            page = 1
        pager = Pager(Post, blog.post_pagesize).order('-date')
        pager.filter('hidden =', False)
        pager.filter('tags =', tag_name)
        posts = pager.fetch(page)
        
        return render('theme/index.html',posts=posts,pager=pager)#prev=prev,next=next)

class show(BaseFront):
    """显示单篇日志"""
    def GET(self, post_url=None):
        import hashlib
        post_id = post_url
        post = Post.get_by_id(int(post_id))
        if not post:
            raise web.notfound()
        
        fullpath = web.ctx.home + web.ctx.fullpath
        check = "%s%s" % (fullpath, post.key())
        checksum = hashlib.sha1(check).hexdigest()
        
        comments_query = Comment.all().filter('post =', post)
        if blog.comment_sort == 'asc':
            comments_query.order('created')
        else:
            comments_query.order('-created')
        
        comments = comments_query.fetch(blog.comment_pagesize)
        
        return render('theme/show.html',
                      post=post,
                      checksum=checksum,
                      comments=comments)

class feed(BaseFront):
    """种子输出"""
    def GET(self):
        from util.feedgenerator import Atom1Feed
        
        blog = Blog.get()
        blog_home = web.ctx.home
        feed = Atom1Feed(
            title=blog.name,
            link=blog_home,
            description=blog.description,
        )
        posts = Post.all().filter('hidden =', False).order('-date').fetch(10)
        for post in posts:
            if post.category:
                category = (post.category.name,)
            else:
                category = ()
            if post.tags:
                category = category + tuple(post.tags)
            feed.add_item(title=post.title,
                          link=blog_home + post.getUrl(),
                          description=post.content,
                          pubdate=post.date,
                          categories=category
                          )
        web.header('Content-Type', 'application/atom+xml')
        return feed.writeString('utf-8')
