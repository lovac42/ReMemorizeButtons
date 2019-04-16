# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


# This is not a stand alone addon and requires ReMemorize for scheduling.
# Logging, Fuzz, and load balance are performed by ReMemorize


import sys
from aqt import mw
from anki.hooks import wrap
from aqt.reviewer import Reviewer
from anki.sched import Scheduler
from anki.lang import _
from .rememorize_btn import *
from .const import *


rBtn=ReMemButtons()


def answerButtons(sched, card, _old):
    cnt=_old(sched, card)
    rBtn.setCount(cnt)
    if not rBtn.check(card):
        return cnt
    for i in range (2,5): #who is calling?
        try:
            f=sys._getframe(i)
        except ValueError: break
        if f.f_code.co_name==ANS_BTN_TAG:
            return cnt
    return rBtn.getExtraCount()


def answerButtonList(rev, _old):
    list=_old(rev)
    if not rBtn.check():
        return list
    i=1;
    for s,t in rBtn.btns:
        list+=((rBtn.count+i, _(s)),)
        i+=1
    return list


def buttonTime(rev, ease, _old):
    if not rBtn.check(ease=ease):
        return _old(rev, ease)
    days=rBtn.getDays(ease) or "errore"
    return '<span class=nobold>%sd</span><br>'%days 


def answerCard(sched, card, ease, _old):
    if not rBtn.check(ease=ease):
        return _old(sched, card, ease)
    try:
        rBtn.reschedule(card,ease)
    except TypeError: pass



#For Anki20
def keyHandler(rev, evt, _old):
    key=unicode(evt.text())
    for i in rBtn.getKeys():
        if key==str(i):
            return rev._answerCard(int(key))
    return _old(rev, evt)


#For Anki21
def shortcutKeys(rev, _old):
    arr=_old(rev)
    for i in rBtn.getKeys():
        t=(str(i),lambda i=i: rev._answerCard(i))
        arr.append(t)
    return arr



Reviewer._answerButtonList = wrap(Reviewer._answerButtonList, answerButtonList, 'around')
Reviewer._buttonTime = wrap(Reviewer._buttonTime, buttonTime, 'around')
Scheduler.answerCard = wrap(Scheduler.answerCard, answerCard, 'around')
Scheduler.answerButtons = wrap(Scheduler.answerButtons, answerButtons, 'around')


if ANKI21:
    from anki.schedv2 import Scheduler as SchedulerV2
    SchedulerV2.answerCard = wrap(SchedulerV2.answerCard, answerCard, 'around')
    SchedulerV2.answerButtons = wrap(SchedulerV2.answerButtons, answerButtons, 'around')
    Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, shortcutKeys, 'around')
else:
    Reviewer._keyHandler = wrap(Reviewer._keyHandler, keyHandler, 'around')

