# -*- coding: utf-8 -*-

from google.appengine.api import memcache

from post.models import Post, Tag
from category.models import Category
from comment.models import Comment
from links.models import Link

class Widget(object):
    """博客装饰"""
    params = None
    
    def __init__(self, params=None):
        self.params = params
    
    def name(self):
        return ''

default_widgets = ['categories', 'recent_entries', 'recent_comments',
            'hot_tags', 'links', 'custom_html']

class categories(Widget):
    """文章分类装饰"""
    key_name = 'categories'
    def name(self):
        return u"文章分类"
    
    def body(self):
        content = memcache.get('widget_category_list')
        if not content:
            category_list = Category.all().order('sort')
        
            content = []
            write = content.append
            write('<ul>')
            for category in category_list:
                write('<li><a href="%s">%s</a>(%s)</li>' % 
                        (category.getUrl(), category.name, category.count))
            write('</ul>')
            content = '\n'.join(content)
            memcache.set('widget_category_list', content)
        
        return content

class recent_entries(Widget):
    """最新文章装饰"""
    key_name = 'recent_entries'
    def name(self):
        return u"最新文章"
    
    def body(self):
        content = memcache.get('widget_post_list')
        if not content:
            post_list = Post.all().filter('hidden =',False)\
                            .order('-date').fetch(10)
        
            content = []
            write = content.append
            write('<ul>')
            for post in post_list:
                write('<li><a href="%s">%s</a></li>' %
                            (post.getUrl(), post.title))
            write('</ul>')
            content = '\n'.join(content)
            memcache.set('widget_post_list', content)
        
        return content

class recent_comments(Widget):
    """新新评论"""
    key_name = 'recent_comments'
    def name(self):
        return u"最新评论"
    
    def body(self):
        content = memcache.get('widget_comments')
        if not content:
            comments = Comment.all().order('-created').fetch(10)
            
            content = []
            write = content.append
            write('<ul>')
            for comment in comments:
                write("""<li>
                <span class="author"><a href="%s" target="_blank">%s</a></span>
                <a href="%s#cmt">%s</a>
                </li>""" % (comment.homepage, comment.name, 
                comment.post.getUrl(), comment.content))
            write('</ul>')
            content = '\n'.join(content)
            memcache.set('widget_comments', content)
        
        return content

class hot_tags(Widget):
    """热门Tag云图"""
    key_name = 'hot_tags'
    def name(self):
        return u"热门Tag"
    
    def body(self):
        content = memcache.get('widget_tag_list')
        if not content:
            tag_list = Tag.all().order('count').fetch(10)
            
            content = []
            write = content.append
            for tag in tag_list:
                write('<span class=""><a href="%s">%s</a></span>' %
                        (tag.getUrl(), tag.name))
            content = '\n'.join(content)
            memcache.set('widget_tag_list', content)
        
        return content

class links(Widget):
    """友情链接装饰"""
    key_name = 'links'
    def name(self):
        return u"友情链接"
    
    def body(self):
        content = memcache.get('widget_links')
        if not content:
            links = Link.all().order('sort')
            
            content = []
            write = content.append
            write('<ul>')
            for link in links:
                write('<li><a href="%s" target="_blank">%s</a></li>' %
                        (link.url, link.name))
            write('</ul>')
            content = '\n'.join(content)
            memcache.set('widget_links', content)
        
        return content

class custom_html(Widget):
    """自定义HTML装饰"""
    def name(self):
        return u"自定义HTML"
    
    def body(self):
        return ''
