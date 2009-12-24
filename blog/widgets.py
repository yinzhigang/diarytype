# -*- coding: utf-8 -*-

from StringIO import StringIO

from post.models import Post, Tag
from category.models import Category
from comment.models import Comment

class Widget(object):
    """博客装饰"""
    params = None
    
    def __init__(self, params=None):
        self.params = params
    
    def name(self):
        return ''

default_widgets = ['categories', 'recent_entries', 'recent_comments',
            'hot_tags', 'custom_html']

class categories(Widget):
    """文章分类装饰"""
    key_name = 'categories'
    def name(self):
        return u"文章分类"
    
    def body(self):
        category_list = Category.all().order('sort')
        
        content = []
        write = content.append
        write('<ul>')
        for category in category_list:
            write('<li><a href="%s">%s</a>(%s)</li>' % 
                    (category.getUrl(), category.name, category.count))
        write('</ul>')
        
        return '\n'.join(content)

class recent_entries(Widget):
    """最新文章装饰"""
    key_name = 'recent_entries'
    def name(self):
        return u"最新文章"
    
    def body(self):
        post_list = Post.all().filter('hidden =',False)\
                        .order('-date').fetch(10)
        
        content = []
        write = content.append
        write('<ul>')
        for post in post_list:
            write('<li><a href="%s">%s</a></li>' %
                        (post.getUrl(), post.title))
        write('</ul>')
        
        return '\n'.join(content)

class recent_comments(Widget):
    """新新评论"""
    key_name = 'recent_comments'
    def name(self):
        return u"最新评论"
    
    def body(self):
        comments = Comment.all().order('-created').fetch(10)
        
        content = []
        write = content.append
        write('<ul>')
        for comment in comments:
            write("""<li>
            <span class="author"><a href="%s" target="_blank">%s</a></span>
            <a href="%s#cmt">%s</a>
            </li>""" % (comment.homepage, comment.name, comment.post.getUrl(), comment.content))
        write('</ul>')
        
        return '\n'.join(content)

class hot_tags(Widget):
    """热门Tag云图"""
    key_name = 'tags'
    def name(self):
        return u"热门Tag"
    
    def body(self):
        tag_list = Tag.all().order('count').fetch(10)
        
        content = []
        write = content.append
        for tag in tag_list:
            write('<span class=""><a href="%s">%s</a></span>' %
                    (tag.getUrl(), tag.name))
        
        return '\n'.join(content)

class custom_html(Widget):
    """自定义HTML装饰"""
    def name(self):
        return u"自定义HTML"
    
    def body(self):
        return ''
