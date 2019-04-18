# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.utils import showInfo
from anki.hooks import addHook
# from anki.lang import _
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
        addHook(ADDON_NAME+".configLoaded", self.onConfigLoaded)
        addHook(ADDON_NAME+".configUpdated", self.onConfigLoaded)
        addHook("rememorize.configLoaded", self.onRememorizeLoaded)


    def onConfigLoaded(self):
        self.btns=self.conf.get('buttons',DEFAULT_BTN)


    def onRememorizeLoaded(self):
        "signal that rememorize was installed"
        self.remem_loaded=True


    def getButtonTime(self, ease):
        if ease<5: return ''
        p=self.conf.get("button_text_prefix","R: ")
        if self.conf.get("show_btn_time_in_days",False):
            d=self.getDays(ease)
            if not d:
                #tobe colorize red with css
                return '<span class="nobold rem_error">ERROR!</span><br>'
            s='%dd'%d
        else:
            s=self.btns[ease-5][1] #zero based
        return '<span class="nobold rem_time%d">%s%s</span><br>'%(ease-4,p,s)


    def getDays(self, ease):
        if ease<5: return 'x' #avoid V1 dynamic btn mappings
        str=self.btns[ease-5][1]
        neg=False
        if str=='-0':
            return str
        elif str[0]=='-': #negative num, change due, keep interval
            neg=True
            str=str[1:]
        elif str=='0':
            return '0' #str to bypass checks for null
        try:
            days=int(parseDate(str))
            if neg: days = - days
        except TypeError: return
        except ValueError: return
        return days


    def getKeys(self):
        L=len(self.btns)
        if not L:
            return (None,)
        return range(5,6+L)


    def getCount(self):
        return max(4,self.count)

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
        return self.getCount()+len(self.btns)


    def reschedule(self, card, ease):
        due=card.due
        days=self.getDays(ease)
        if days==None:
            showInfo("""
Past due or invalid parsing string,<br>
The reviewer will drop this card,<br>
but you will see it again when it<br>
comes back around. NO CHANGES HAS BEEN MADE.
""")
            return
        elif days=='-0':
            showInfo("PC LOAD A4!")
            return
        elif days=='x': #V1 dyn good, ez btn
            if self.conf.get('cascade_easy_button',False):
                c=mw.reviewer.card
                mw.col.sched.answerCard(c,self.count)
                if self.conf.get('show_tooltip',True):
                    msg="Key %d was cascaded to %d"%(ease,self.count)
                    d=self.conf.get('tooltip_duration',1200)
                    tooltipHint(msg,d/1.5)
            else:
                showInfo("""
Key %d on V1 is not used here, Mr.Reviewer will<br>
drop the current card. But you will see it again when<br>
it comes back around. NO CHANGES HAS BEEN MADE.<br>
Set "cascade_easy_button" to true in config to avoid this message.
"""%ease)
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
            d=self.conf.get('tooltip_duration',1200)
            d=max(d,400) #idiot proof enough?
            mw.progress.timer(20,
                lambda:schedConfirm(card.id,card.ivl,due,d),False)


    def showAnsConfirm(self, ease):
        if self.conf.get('show_answer_confirmation',False):
            BTN_KEY=((1,3,3,3),
                     (1,3,4,4),
                     (1,2,3,4))
            k=BTN_KEY[self.count-2][ease-1]-1
            msg="%s!"%("Again","Hard","Good","Easy")[k]
            d=self.conf.get('tooltip_duration',1200)
            tooltipHint(msg,d/1.5)

