# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.2 (Prototype version)


# This is not a stand alone addon and requires ReMemorize for scheduling.
# Logging, Fuzz, and load balance are performed by ReMemorize
# Only new cards, review cards are blocked to prevent abuse.

# Please restart Anki if switching between V1 & V2,
# profile initialization values differ between them.
# In other words, don't screw around.


# -----------------------------
#  USER CONFIGS
# -----------------------------

# add-remove numbers/descriptions as needed
BUTTON_DAYS = ( 10, 15, 20, 40 )
BUTTON_DESC = ('Blah', 'Meh', 'Wowza', 'Wordless')

DISALLOW_FILTERED_DECKS = True

# -----------------------------


import sys, aqt
from aqt import mw
from anki.hooks import wrap, runHook, addHook
from aqt.reviewer import Reviewer
from anki.sched import Scheduler
from anki.lang import _
from anki import version
ANKI21 = version.startswith("2.1.")

TAG='_answerButtonList' if ANKI21 else 'answerButtonList'


#Global
offMode=False
nBtn=4

def onProfileLoaded():
    global nBtn
    nBtn=4 if mw.col.sched.name=="std2" else 3
addHook('profileLoaded', onProfileLoaded)



def answerButtons(sched, card, _old):
    global offMode, nBtn
    nBtn=_old(sched, card)
    if card.type in (2,3) or \
    (DISALLOW_FILTERED_DECKS and card.odid):
        offMode=True
        return nBtn

    for i in range (2,5): #who is calling?
        try:
            f=sys._getframe(i)
        except ValueError: break
        if f.f_code.co_name==TAG:
            return nBtn

    offMode=False
    return nBtn+len(BUTTON_DAYS)



def answerButtonList(rev, _old):
    list=_old(rev)
    if offMode:
        return list
    i=1;
    for s in BUTTON_DESC:
        list+=((nBtn+i, _(s)),)
        i+=1
    return list



def buttonTime(rev, ease, _old):
    if ease<=nBtn or offMode:
        return _old(rev, ease)
    days=BUTTON_DAYS[ease-nBtn-1]
    return '<span class=nobold>%dd</span><br>'%days



def answerCard(sched, card, ease, _old):
    if ease<=nBtn or offMode:
        return _old(sched, card, ease)
    days=BUTTON_DAYS[ease-nBtn-1]
    runHook('ReMemorize.reschedule', card, days)



#For Anki20
def keyHandler(rev, evt, _old):
    key=unicode(evt.text())
    n=nBtn+1
    for i in range(n,n+len(BUTTON_DAYS)):
        if key==str(i):
            return rev._answerCard(int(key))
    return _old(rev, evt)


#For Anki21
def shortcutKeys(rev, _old):
    arr=_old(rev)
    n=nBtn+1
    for i in range(n,n+len(BUTTON_DAYS)):
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

