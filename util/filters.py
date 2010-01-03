# -*- coding: utf-8 -*-

import datetime
import pytz

from blog.models import blog

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    """Template filter, 格式化日期时间"""
    timezone = blog.timezone
    tz = pytz.timezone(timezone)
    try:
        return value.replace(tzinfo=pytz.utc).astimezone(tz).strftime(format)
    except:
        return ''
