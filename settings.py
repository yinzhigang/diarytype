# -*- coding: utf-8 -*-

import os

urls = (
    '/admin/?', 'blog.admin.dashboard',
    
    '/admin/posts', 'post.admin.posts',
    '/admin/post/new', 'post.admin.edit',
    '/admin/post/edit/(\d+)', 'post.admin.edit',
    '/admin/post/delete/(\d+)', 'post.admin.delete',
    
    '/admin/comments', 'comment.admin.comments',
    
    '/admin/categories', 'category.admin.categories',
    '/admin/category/new', 'category.admin.edit',
    '/admin/category/edit/(\d+)', 'category.admin.edit',
    '/admin/category/delete/(\d+)', 'category.admin.delete',
    
    '/admin/links', 'links.admin.links',
    '/admin/link/new', 'links.admin.edit',
    '/admin/link/edit/(\d+)', 'links.admin.edit',
    '/admin/link/delete/(\d+)', 'links.admin.delete',
    
    '/admin/theme', 'theme.admin.theme',
    '/admin/theme/widget', 'theme.admin.widget',
    '/admin/theme/widget/init', 'theme.admin.init_widget',
    
    '/admin/setting', 'blog.admin.setting',
    '/admin/setting/clear_cache', 'blog.admin.clear_cache',
    '/admin/import', 'blog.admin.import_wordpress',
    
    '/feed', 'post.feed',
    
    '/comment', 'comment.comment',
    
    '/theme/(\w+)/(.+)', 'theme.theme_file',
    
    '/category/(.*)', 'post.category_post',
    '/tag/(.*)', 'post.tag_post',
    
    '/', 'post.posts',
    '/post/(\d+)', 'post.show',
)

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')

ROOT = os.path.dirname(__file__)

ADMIN_TEMPLATE_DIR = os.path.join(ROOT, 'templates/admin')
THEME_TEMPLATE_DIR = os.path.join(ROOT, 'templates/theme')

EXTRA_PATHS = [
  os.path.join(ROOT, 'pytz.zip'),
]
