# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import sys
from aqt import mw
from anki.hooks import wrap
from aqt.reviewer import Reviewer
from anki.sched import Scheduler
from anki.lang import _
from .rememorize_btn import *
from .const import *


rBtn=ReMemButtons()



#SCHEDULER
def wrap_answerButtons(sched, card, _old):
    cnt=_old(sched, card)

    rBtn.reset(cnt)
    rBtn.setButtons(card)
    if not rBtn.check(card):
        return cnt

    # Used to get around V1's dynamic 3-4 buttons.
    for i in range (2,5): #who is calling?
        try:
            f=sys._getframe(i)
        except ValueError: break
        if f.f_code.co_name in BTN_CNT_BYPASS:
            return cnt
    return rBtn.getExtraCount()


def wrap_answerButtonList(rev, _old):
    list=_old(rev)
    if not rBtn.check():
        return list
    i=rBtn.getCount()+1
    for s,t in rBtn.btns:
        list+=((i, _(s)),)
        i+=1
    return list


def wrap_buttonTime(rev, ease, _old):
    if not rBtn.check(ease=ease):
        return _old(rev, ease)
    return rBtn.getButtonTime(ease)


def wrap_answerCard(sched, card, ease, _old):
    if not rBtn.check(ease=ease):
        ret=_old(sched, card, ease)
        rBtn.showAnsConfirm(ease)
        return ret
    try:
        rBtn.reschedule(card,ease)
    except TypeError: pass



def wrap_constrainedIvl(sched, ivl, conf, prev, fuzz=False, _old=None):
    nx=rBtn.alt_sched.hasSavedIvl()
    if nx:
        return nx
    if sched.name=="std":
        return _old(sched, ivl, conf, prev)
    return _old(sched, ivl, conf, prev, fuzz)



def wrap_rescheduleLapse(sched, card, _old):
    "Ensures proper EF logging for fail btn"
    delay=_old(sched,card)
    if rBtn.alt_sched.isReschedulable(card):
        card.factor=rBtn.alt_sched.meta_card.getFactor(card.factor)
    return delay


def wrap_rescheduleRev(sched, card, ease, early=False, _old=None):
    "Ensures proper EF logging for pass btns"
    if sched.name=="std":
        ret=_old(sched, card, ease) #using _old ensures load order
    else:
        ret=_old(sched, card, ease, early)
    if rBtn.alt_sched.isReschedulable(card):
        card.factor=rBtn.alt_sched.meta_card.getFactor(card.factor)
    return ret


def wrap_rescheduleNew(sched, card, conf, early, _old):
    "initialize new cards, then add modifier"
    ret=_old(sched, card, conf, early)
    mod=rBtn.alt_sched.getModifier()
    if mod: #Reschedulable by default
        card.ivl=max(1,int(card.ivl*mod))
        card.due=sched.today+card.ivl
    return ret


def wrap_rescheduleAsRev(sched, card, conf, early, _old):
    "when cards graduates, we are limiting to lapsed cards only"
    nx=rBtn.alt_sched.hasSavedIvl()
    if nx and rBtn.alt_sched.isReschedulable(card):
        if card.type in (2,3): #rev only
            card.ivl=nx
            if sched.name=="std":
                card.odue=sched.today+nx #odue will be set to due on _old
            else:
                card.due=sched.today+nx
    #Fuzz is applied after _old
    _old(sched, card, conf, early)


#Renamed _lapseIvl on v2
def wrap_nextLapseIvl(sched, card, conf, _old):
    "Sets the new lapsed ivl when a card lapses due to extremely small modifier button"
    ret=_old(sched, card, conf) #trigger other addons
    nx=rBtn.alt_sched.hasSavedIvl()
    if nx: #Reschedulable by default
        ret=max(conf['minInt'],nx)
    return ret





# ---------------
# Hotkeys
# ---------------


#For Anki20
def wrap_keyHandler(rev, evt, _old): #called 1st
    key=unicode(evt.text())
    for i in rBtn.getKeys():
        if key==str(i):
            return rev._answerCard(i)
    return _old(rev, evt)


#For Anki21
def wrap_shortcutKeys(rev, _old):
    arr=_old(rev)
    for i in rBtn.getKeys():
        t=(str(i),lambda i=i: rev._answerCard(i))
        arr.append(t)
    return arr



Scheduler.answerCard = wrap(Scheduler.answerCard, wrap_answerCard, 'around')
Scheduler.answerButtons = wrap(Scheduler.answerButtons, wrap_answerButtons, 'around')
Scheduler._constrainedIvl = wrap(Scheduler._constrainedIvl, wrap_constrainedIvl, 'around')
Scheduler._rescheduleNew = wrap(Scheduler._rescheduleNew, wrap_rescheduleNew, 'around')
Scheduler._rescheduleRev = wrap(Scheduler._rescheduleRev, wrap_rescheduleRev, 'around')
Scheduler._nextLapseIvl = wrap(Scheduler._nextLapseIvl, wrap_nextLapseIvl, 'around')
Scheduler._rescheduleAsRev = wrap(Scheduler._rescheduleAsRev, wrap_rescheduleAsRev, 'around')
Scheduler._rescheduleLapse = wrap(Scheduler._rescheduleLapse, wrap_rescheduleLapse, 'around')

if ANKI21:
    from anki.schedv2 import Scheduler as SchedulerV2
    SchedulerV2.answerCard = wrap(SchedulerV2.answerCard, wrap_answerCard, 'around')
    SchedulerV2.answerButtons = wrap(SchedulerV2.answerButtons, wrap_answerButtons, 'around')
    SchedulerV2._constrainedIvl = wrap(SchedulerV2._constrainedIvl, wrap_constrainedIvl, 'around')
    SchedulerV2._rescheduleNew = wrap(SchedulerV2._rescheduleNew, wrap_rescheduleNew, 'around')
    SchedulerV2._rescheduleRev = wrap(SchedulerV2._rescheduleRev, wrap_rescheduleRev, 'around')
    SchedulerV2._lapseIvl = wrap(SchedulerV2._lapseIvl, wrap_nextLapseIvl, 'around')
    SchedulerV2._rescheduleAsRev = wrap(SchedulerV2._rescheduleAsRev, wrap_rescheduleAsRev, 'around')
    SchedulerV2._rescheduleLapse = wrap(SchedulerV2._rescheduleLapse, wrap_rescheduleLapse, 'around')

    Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, wrap_shortcutKeys, 'around')
else:
    Reviewer._keyHandler = wrap(Reviewer._keyHandler, wrap_keyHandler, 'around')
Reviewer._answerButtonList = wrap(Reviewer._answerButtonList, wrap_answerButtonList, 'around')
Reviewer._buttonTime = wrap(Reviewer._buttonTime, wrap_buttonTime, 'around')

