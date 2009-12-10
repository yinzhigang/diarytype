#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# Diary Type - The blog system for Google App Engine.
# Copyright (C) 2009 yinzhigang <sxin.net AT gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
###############################################################################
import web

from settings import urls
from util.template import render

app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'world'
        return 'hello ' + name

if __name__ == "__main__":
    app.cgirun()
