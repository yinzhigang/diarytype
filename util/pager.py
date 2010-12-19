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
from __future__ import division
from math import ceil
from math import floor

class Pager(object):
    """Pager for GAE Model"""
    def __init__(self, model_class, maxPrePage=10):
        self._model_class = model_class
        self._query = self._model_class.all()
        self._maxPrePage = int(maxPrePage)
    
    def filter(self, property_operator, value):
        self._query.filter(property_operator, value)
        return self
    
    def order(self, prop):
        self._query.order(prop)
        return self
    
    def fetch(self, page=1):
        self._page = int(page)
        self._nbResults = self._query.count()
        offset = (self._page - 1) * self._maxPrePage
        results = self._query.fetch(self._maxPrePage, offset)
        return results
    
    def getPage(self):
        """获取当前所处分页"""
        return self._page
    
    def getFirstPage(self):
        return 1
    
    def getLastPage(self):
        # if not self._last_page:
        #     self._last_page = ceil(self._nbResults / self._maxPrePage)
        # return int(self._last_page)
        last_page = ceil(self._nbResults / self._maxPrePage)
        return int(last_page)
    
    def getNextPage(self):
        return min(self._page + 1, self.getLastPage())

    def getPreviousPage(self):
        return max(self._page - 1, self.getFirstPage())

    def isLastPage(self):
        return self._page >= self.getLastPage()
        
    def isFirstPage(self):
        return self._page <= self.getFirstPage()
    
    def getLinks(self, nb_links=5):
        links = []
        tmp = self._page - floor(nb_links / 2)
        check = self.getLastPage() - nb_links + 1
        limit = check if check > 0 else 1 # check > 0 ? check : 1
        begin = (limit if tmp > limit else tmp) if tmp > 0 else 1 # tmp > 0 ? (tmp > limit ? limit : tmp) : 1
        
        i = int(begin)
        while (i < begin + nb_links and i <= self.getLastPage()):
            links.append(i)
            i = i + 1
        
        return links
