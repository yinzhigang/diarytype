# -*- coding: utf-8 -*-

import os

urls = (
    '/admin/?', 'blog.admin.setting',
    
    '/admin/posts', 'post.admin.posts',
    '/admin/post/new', 'post.admin.post',
    '/admin/post/edit/(\d+)', 'post.admin.post',
    '/admin/post/delete/(\d+)', 'post.admin.delete',
    
    '/admin/setting', 'blog.admin.setting',
    '/admin/import', 'blog.admin.import_wordpress',
    
    '/theme/(\w+)/(.+)', 'theme.theme_file',
    
    '/', 'post.posts',
    '/post/(\d+)', 'post.show',
    '/(.*)', 'hello',
)

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

ROOT = os.path.dirname(__file__)

ADMIN_TEMPLATE_DIR = os.path.join(ROOT, 'templates/admin')
THEME_TEMPLATE_DIR = os.path.join(ROOT, 'templates/theme')
