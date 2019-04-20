# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

# Some code from ReMemorize.utils.py and modified


from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo
from anki.lang import _
import datetime
import aqt.utils


def schedConfirm(id, ivl, due, duration, txt=''):
    msg=None
    card=mw.col.getCard(id)
    if card.ivl==0:
        msg="Forgotten card"
    elif card.ivl!=ivl:
        msg="Reschedule %d days"%card.ivl
    elif card.due!=due:
        msg="Card due date changed"
    if msg:
        tooltipHint(txt+'<br>'+msg, duration)


def tooltipHint(msg, period):
    tooltip(_(msg), period=period)
    aw=mw.app.activeWindow() or mw
    aqt.utils._tooltipLabel.move(
        aw.mapToGlobal(QPoint( aw.width()/2 -100, aw.height() -200)))
        #wish we could track eye movement and reposition accordingly :/


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

