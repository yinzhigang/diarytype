# -*- coding: utf-8 -*-

import web

from blog.models import Blog
from util.template import render
from util import requires_admin

class dashboard(object):
    """后台管理首页"""
    @requires_admin
    def GET(self):
        pass

class setting(object):
    @requires_admin
    def GET(self):
        """系统设置表单"""
        blog = Blog.get()
        
        return render('admin/setting.html',blog=blog)
    
    @requires_admin
    def POST(self):
        """保存博客信息"""
        inp = web.input()
        
        blog = Blog.get()
        blog.name = inp.name
        blog.description = inp.description
        blog.custom_header = inp.custom_header
        blog.save()
        
        raise web.seeother('/admin/setting')

xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <!-- This is a WordPress eXtended RSS file generated by Micolog as an export of your blog. -->
        <!-- It contains information about your blog's posts, comments, and categories. -->
        <!-- You may use this file to transfer that content from one site to another. -->
        <!-- This file is not intended to serve as a complete backup of your blog. -->

        <!-- To import this information into a WordPress blog follow these steps. -->
        <!-- 1. Log into that blog as an administrator. -->
        <!-- 2. Go to Manage: Import in the blog's admin panels. -->
        <!-- 3. Choose "WordPress" from the list. -->
        <!-- 4. Upload this file using the form provided on that page. -->
        <!-- 5. You will first be asked to map the authors in this export file to users -->
        <!--    on the blog.  For each author, you may choose to map to an -->
        <!--    existing user on the blog or to create a new user -->
        <!-- 6. WordPress will then import each of the posts, comments, and categories -->
        <!--    contained in this file into your blog -->

        <!-- generator="Micolog" -->
        <rss version="2.0"
        xmlns:content="http://purl.org/rss/1.0/modules/content/"
        xmlns:excerpt="http://wordpress.org/export/1.0/excerpt/"
        xmlns:wfw="http://wellformedweb.org/CommentAPI/"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:wp="http://wordpress.org/export/1.0/"
        >

        <channel>
        <title>Micolog</title>
        <link>http://localhost:8082</link>
        <description></description>
        <pubDate>星, 9 十二月 2009 15:30:18 +0000</pubDate>
        <generator>micolog</generator>
        <language>en</language>
        <wp:wxr_version>1.0</wp:wxr_version>
        <wp:base_site_url>http://localhost:8082</wp:base_site_url>
        <wp:base_blog_url>http://localhost:8082</wp:base_blog_url>

        <wp:category><wp:category_nicename>php</wp:category_nicename><wp:category_parent></wp:category_parent><wp:cat_name><![CDATA[PHP]]></wp:cat_name></wp:category>
        <wp:category><wp:category_nicename>python</wp:category_nicename><wp:category_parent></wp:category_parent><wp:cat_name><![CDATA[Python]]></wp:cat_name></wp:category>
        <wp:category><wp:category_nicename>gae</wp:category_nicename><wp:category_parent></wp:category_parent><wp:cat_name><![CDATA[Google App Enging]]></wp:cat_name></wp:category>

        <wp:tag><wp:tag_slug>gae</wp:tag_slug><wp:tag_name><![CDATA[gae]]></wp:tag_name></wp:tag>
        <wp:tag><wp:tag_slug>wordpress</wp:tag_slug><wp:tag_name><![CDATA[wordpress]]></wp:tag_name></wp:tag>

        <item>
        <title>欢迎使用Micolog</title>
        <link>/2009/12/9/wellcome.html</link>
        <pubDate>2009-12-09 09:18:35.103134</pubDate>
        <dc:creator><![CDATA[None]]></dc:creator>

        <category><![CDATA[Google App Enging]]></category>
        <category domain="category" nicename="gae"><![CDATA[Google App Enging]]></category>

        <category><![CDATA[gae]]></category>
        <category domain="tag" nicename="gae"><![CDATA[gae]]></category>
        <category><![CDATA[wordpress]]></category>
        <category domain="tag" nicename="wordpress"><![CDATA[wordpress]]></category>
        <guid isPermaLink="false">/2009/12/9/wellcome.html</guid>
        <description></description>
        <content:encoded><![CDATA[<p>欢迎使用micolog. 这是您的第一篇博客. 您可以修改或删除这篇文章，开始您精彩的独立Blog之旅。</p>]]></content:encoded>
        <excerpt:encoded><![CDATA[abcdefg]]></excerpt:encoded>
        <wp:post_id>1</wp:post_id>
        <wp:post_date>2009-12-09 09:18:35.103134</wp:post_date>
        <wp:post_date_gmt>星, 9 十二月 2009 09:18:35 +0000</wp:post_date_gmt>
        <wp:comment_status>open</wp:comment_status>
        <wp:ping_status>open</wp:ping_status>
        <wp:post_name>wellcome</wp:post_name>
        <wp:status>publish</wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type>post</wp:post_type>
        <wp:post_password></wp:post_password>

        </item>

        </channel>
        </rss>
"""

import xml.sax
from xml.sax.handler import *
from StringIO import StringIO

class MyHandler(ContentHandler):
    isTitle=""
    title=""
    ns = []
    def startElement(self,name,attrs):
        print name
        if name=="title":
            self.isTitle=1
    def endElement(self,name):
        if name=="title":
            self.isTitle=""
    def startElementNS(self,name,qname,attrs):
        print name
        self.ns.push(name)
    def endElementNS(self,name,qname):
        pass
    def characters(self,content):
        if self.isTitle:
            self.title+=content

class import_wordpress(object):
    """导入wordpress备份"""
    @requires_admin
    def GET(self):
        ch = MyHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(ch)
        parser.parse(StringIO(xml_content))
        return ch.ns
        