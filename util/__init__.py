# encoding: utf-8

import web
from google.appengine.api import users

def requires_admin(method):
    def wrapper(self, *args, **kwargs):
        if not users.is_current_user_admin():
            home = web.ctx.home
            fullpath = web.ctx.fullpath
            url = users.create_login_url(home + fullpath)
            return web.found(url)
        else:
            from util.template import env
            env.globals['logout_url'] = users.create_logout_url('/')
            return method(self, *args, **kwargs)
    return wrapper

