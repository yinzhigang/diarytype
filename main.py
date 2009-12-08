# -*- coding: utf-8 -*-
import web
from web.contrib.template import render_jinja

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

render = render_jinja(
        'templates',   # Set template directory.
        encoding = 'utf-8',                         # Encoding.
    )


class hello:        
    def GET(self, name):
        if not name: 
            name = 'world'
        return render.hello(name=name)

if __name__ == "__main__":
    app.cgirun()
