# -*- coding: utf-8 -*-

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    """Template filter, 格式化日期时间"""
    try:
        return value.strftime(format)
    except:
        return ''
