# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.utils import tooltip, showInfo
from anki.hooks import addHook
from anki.lang import _
from .config import *
from .const import *
from .utils import *


class ReMemButtons:
    btns=DEFAULT_BTN
    remem_loaded=False
    mode=True
    count=4

    def __init__(self):
        self.conf=Config(ADDON_NAME)
        addHook("rememorize.configLoaded", self.onRememorizeLoaded)


    def onRememorizeLoaded(self):
        "signal that rememorize was installed"
        self.remem_loaded=True


    def getButtonTime(self, ease):
        e=ease-self.count #start from 1
        p=self.conf.get("button_text_prefix","R:")
        if self.conf.get("show_btn_time_in_days",False):
            s=self.getDays(ease) or "errore"
            s+='d'
        else:
            s=self.btns[e-1][1] #zero based
        return '<span class="nobold rem_time%d">%s%s</span><br>'%(e,p,s)


    def getDays(self, ease):
        e=ease-self.count-1
        str=self.btns[e][1]
        neg=False
        if str=='0':
            return '0'
        if str[0]=='-': #negative num, change due, keep interval
            neg=True
            str=str[1:]
        try:
            days=int(parseDate(str))
            if neg: days = - days
        except TypeError: return
        except ValueError: return
        return days


    def getKeys(self):
        #key 1-4 already mapped
        return range(5,5+len(self.btns))


    def setCount(self, cnt):
        self.mode=True
        self.count=cnt


    def check(self, card=None, ease=None):
        "check if card or ease should be processed"
        if not self.remem_loaded or not self.mode:
            return False

        if ease and ease<=self.count:
            return False

        if card:
            if card.ivl > self.conf.get('young_card_ivl',0):
                self.mode=False
            elif card.odid and self.conf.get('disallow_filtered_decks',True):
                self.mode=False
        return self.mode


    def getExtraCount(self):
        "return length of total btns"
        self.btns=self.conf.get('buttons',DEFAULT_BTN)
        return self.count+len(self.btns)


    def reschedule(self, card, ease):
        due=card.due
        days=self.getDays(ease)
        if days==None:
            showInfo("Invalid parse string or past due")
            return
        elif days=='0':
            runHook('ReMemorize.forget', card)
        elif days>0:
            runHook('ReMemorize.reschedule', card, days)
        elif days<0:
            runHook('ReMemorize.changeDue', card, -days)
        else:
            return

        if self.conf.get('show_tooltip',True):
            mw.progress.timer(20,
                lambda:self.schedCheck(card.id,card.ivl,due),False)


    def schedCheck(self, id, ivl, due):
        msg=None
        card=mw.col.getCard(id)
        if card.ivl==0:
            msg="Forgotten card"
        elif card.ivl!=ivl:
            msg="Reschedule %d days"%card.ivl
        elif card.due!=due:
            msg="Due Changed"
        if msg:
            tooltip(_(msg), period=1000)


