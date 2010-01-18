# -*- coding: utf-8 -*-

import os

VERSION = '0.1.0'

urls = (
    '/admin/install', 'blog.admin.install',
    
    '/admin/?', 'blog.admin.dashboard',
    
    '/admin/posts', 'post.admin.posts',
    '/admin/post/new', 'post.admin.edit',
    '/admin/post/edit/(\d+)', 'post.admin.edit',
    '/admin/post/delete/(\d+)', 'post.admin.delete',
    
    '/admin/media', 'media.admin.media_list',
    '/admin/media/upload', 'media.admin.upload',
    '/admin/media/delete/(.*)', 'media.admin.delete',
    
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
    '/admin/theme/change/(\w+)', 'theme.admin.change_theme',
    '/admin/theme/screenshot/(\w+)', 'theme.admin.theme_screenshot',
    '/admin/theme/install', 'theme.admin.install_theme',
    '/admin/theme/delete/(\w+)', 'theme.admin.delete_theme',
    '/admin/theme/widget', 'theme.admin.widget',
    '/admin/theme/widget/init', 'theme.admin.init_widget',
    
    '/admin/setting', 'blog.admin.setting',
    '/admin/setting/habit', 'blog.admin.habit',
    '/admin/setting/clear_cache', 'blog.admin.clear_cache',
    '/admin/import', 'blog.admin.import_wordpress',
    
    '/feed', 'post.feed',
    '/comment', 'comment.comment',
    '/theme/(\w+)/(.+)', 'theme.theme_file',
    '/category/(.*)', 'post.category_post',
    '/media/source/(.*)\..*', 'media.media_source',
    '/media/(.+)/(.*)\..*', 'media.media_thumb',
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
