# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1 (Prototype version)


# This is not a stand alone addon and requires ReMemorize for scheduling.
# Logging, Fuzz, and load balance are performed by ReMemorize

# no hotkey setup yet
# on V1, 3 buttons are displayed as again, hard, good instead of A-G-E


# -----------------------------
#  USER CONFIGS
# -----------------------------

BUTTON_DAYS = ( 10, 15, 20 )

# -----------------------------



from aqt import mw
from anki.hooks import wrap, runHook
from aqt.reviewer import Reviewer
from anki.sched import Scheduler
from anki import version
ANKI21 = version.startswith("2.1.")


#Global
filteredDeck=False
nBtn=1

def answerButtons(sched, card, _old):
    global filteredDeck, nBtn
    nBtn=_old(sched, card)
    if card.odid:
        filteredDeck=True
        return nBtn
    filteredDeck=False
    return nBtn+len(BUTTON_DAYS)

def answerButtonList(rev, _old):
    list=_old(rev)[:nBtn]
    if filteredDeck:
        return list
    return list+(
        (nBtn+1, _('Blah')), 
        (nBtn+2, _('Meh')),
        (nBtn+3, _('Wowza')) )

def buttonTime(rev, ease, _old):
    if ease<=nBtn or filteredDeck:
        return _old(rev, ease)
    days=BUTTON_DAYS[ease-nBtn-1]
    return '<span class=nobold>%dd</span><br>'%days

def answerCard(sched, card, ease, _old):
    if ease<=nBtn or filteredDeck:
        return _old(sched, card, ease)
    days=BUTTON_DAYS[ease-nBtn-1]
    runHook('ReMemorize.reschedule', card, days)


Reviewer._answerButtonList = wrap(Reviewer._answerButtonList, answerButtonList, 'around')
Reviewer._buttonTime = wrap(Reviewer._buttonTime, buttonTime, 'around')
Scheduler.answerCard = wrap(Scheduler.answerCard, answerCard, 'around')
Scheduler.answerButtons = wrap(Scheduler.answerButtons, answerButtons, 'around')


if ANKI21:
    from anki.schedv2 import Scheduler as SchedulerV2
    SchedulerV2.answerCard = wrap(SchedulerV2.answerCard, answerCard, 'around')
    SchedulerV2.answerButtons = wrap(SchedulerV2.answerButtons, answerButtons, 'around')

