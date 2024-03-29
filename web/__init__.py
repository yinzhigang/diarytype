#!/usr/bin/env python
"""web.py: makes web apps (http://webpy.org)"""

from __future__ import generators

__version__ = "0.33"
__author__ = [
    "Aaron Swartz <me@aaronsw.com>",
    "Anand Chitipothu <anandology@gmail.com>"
]
__license__ = "public domain"
__contributors__ = "see http://webpy.org/changes"

import utils, net, http, webapi

from utils import *
from net import *
from http import *
from webapi import *
from application import *

