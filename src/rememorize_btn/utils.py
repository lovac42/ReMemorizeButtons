# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Code from ReMemorize.utils.py and modified


from aqt import mw
# from aqt.utils import tooltip, showInfo
import datetime


def parseDate(days):
    try:
        return getDays(days)
    except ValueError: #non date format
        return days
    except TypeError: #passed date
        return None


def getDays(date_str):
    d=datetime.datetime.today()
    today=datetime.datetime(d.year, d.month, d.day)
    try:
        due=datetime.datetime.strptime(date_str,'%m/%d/%Y')
    except ValueError:
        date_str=date_str+'/'+str(d.year)
        due=datetime.datetime.strptime(date_str,'%m/%d/%Y')
    diff=(due-today).days
    if diff<1: raise TypeError
    return diff

