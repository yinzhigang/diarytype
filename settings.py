# -*- coding: utf-8 -*-

import os

urls = (
    '/admin/?', 'blog.admin.setting',
    
    '/admin/posts', 'post.admin.posts',
    '/admin/post/new', 'post.admin.edit',
    '/admin/post/edit/(\d+)', 'post.admin.edit',
    '/admin/post/delete/(\d+)', 'post.admin.delete',
    
    '/admin/categories', 'category.admin.categories',
    '/admin/category/new', 'category.admin.edit',
    '/admin/category/edit/(\d+)', 'category.admin.edit',
    '/admin/category/delete/(\d+)', 'category.admin.delete',
    
    '/admin/comments', 'comment.admin.comments',
    
    '/admin/theme', 'theme.admin.theme',
    '/admin/theme/widget', 'theme.admin.widget',
    '/admin/theme/widget/init', 'theme.admin.init_widget',
    
    '/admin/setting', 'blog.admin.setting',
    '/admin/setting/clear_cache', 'blog.admin.clear_cache',
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
