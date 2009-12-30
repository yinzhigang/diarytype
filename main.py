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
import wsgiref

import settings

app = web.application(settings.urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'world'
        return 'hello ' + name

def real_main():
    wsgiapp = app.wsgifunc()
    wsgiref.handlers.CGIHandler().run(wsgiapp)
    # run_wsgi_app(wsgiapp)

def profile_main():
    # This is the main function for profiling 
    # We've renamed our original main() above to real_main()
    import cProfile, pstats
    import logging
    import cStringIO as StringIO
    prof = cProfile.Profile()
    prof = prof.runctx("real_main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    # print "<pre>"
    # stats = pstats.Stats(prof)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    # print "</pre>"
    logging.info("Profile data:\n%s", stream.getvalue())

main = real_main

if __name__ == "__main__":
    main()
