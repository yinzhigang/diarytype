# -*- coding: utf-8 -*-
import web

import settings
from util.template import render

app = web.application(settings.urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'world'
        return 'hello ' + name

if __name__ == "__main__":
    app.cgirun()
