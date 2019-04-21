# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.utils import showInfo
from anki.utils import fmtTimeSpan
from anki.hooks import addHook
# from anki.lang import _
from .alt_sched import *
from .config import *
from .const import *
from .utils import *
from .signals import *


class ReMemButtons:
    btns=DEFAULT_BTN
    rememorize=None
    mode=True
    write_btns=0 #offset marker
    real_ease=0 #for tooltip
    count=4 #total actual anki btn cnt


    def __init__(self):
        self.conf=Config(ADDON_NAME)
        self.alt_sched=AltScheduler(self.conf)
        addHook("rememorize.configLoaded", self.onRememorizeLoaded)


    def onRememorizeLoaded(self):
        "signal that rememorize was installed"
        self.rememorize=ReMemorizeScheduler(self.conf)


    def reset(self, n=4):
        self.mode=True
        self.btns=[]
        self.setCount(n)


    def setButtons(self, card):
        if self.alt_sched.isReschedulable(card):
            if card.type in (0,1):
                key='new_modifier_buttons'
            elif card.queue in (1,3):
                key='lrn_modifier_buttons'
            else:
                key='rev_modifier_buttons'
            w=self.conf.get(key,None)
            self.write_btns=len(w)
            self.btns.extend(w)

        if self.rememorize and self.alt_sched.isDynReschedulable(card):
            r=self.conf.get('rememorize_buttons',DEFAULT_BTN)
            self.btns.extend(r)


    def getButtonType(self, ease):
        if self.conf.get('enable_write_access',False) and \
        self.write_btns>ease-5:
            return MODIFIER_BTN
        return REMEMORIZE_BTN


    def getButtonTime(self, ease):
        if ease<5:
            return ''

        if self.getButtonType(ease)==MODIFIER_BTN:
            return self._getModifierTime(ease)

        if self.rememorize:
            self.rememorize.setButtons(self.btns)
            return self.rememorize.getTimeString(ease)


    def _getModifierTime(self, ease):
        card=mw.reviewer.card
        modifier=int(self.btns[ease-5][1])/100.0 #zero based
        self.alt_sched.setModifier(modifier)
        if card.queue in(0,1,3):
            ivl=self.alt_sched.getLrnBtnIvl(card,self.count)
        else:
            ivl=self.alt_sched.getBtnIvl(card,self.count)
        s=fmtTimeSpan(ivl*86400,short=True)
        return '<span class="nobold rem_modifier rem_time%d">%s</span><br>'%(ease-MAX_DEF_BTN,s)


    def getKeys(self):
        L=len(self.btns)
        if not L:
            return (None,)
        return range(5,6+L)


    def setCount(self, cnt):
        self.count=cnt

    def getCount(self):
        return max(4,self.count)

    def getExtraCount(self):
        "return length of total btns"
        return self.getCount()+len(self.btns)


    def check(self, card=None, ease=None):
        "check if card or ease should be processed"
        if not self.btns or not self.mode:
            return False

        if ease and ease<=self.count:
            return False

        if card:
            if card.queue>3: #q4=preview
                self.mode=False
            elif card.ivl > self.conf.get('young_card_ivl',0):
                self.mode=False
            elif card.odid and self.conf.get('disallow_filtered_decks',True):
                self.mode=False
        return self.mode



    def reschedule(self, card, ease):
        if ease<5: #V1 dyn good, ez btn
            return self.handleMissing4thBtn(card,ease)

        if self.getButtonType(ease)==MODIFIER_BTN:
            self.real_ease=ease #save for tooltip usage
            modifier=int(self.btns[ease-5][1])/100.0 #zero based
            if card.queue in (0,1,3):
                ease=self.count #find ez btn
            return self.alt_sched.reschedule(card,ease,modifier)

        if self.rememorize:
            self.rememorize.setButtons(self.btns)
            return self.rememorize.reschedule(card,ease)



    def handleMissing4thBtn(self, card, ease):
        if self.conf.get('cascade_easy_button',False):
            mw.col.sched.answerCard(card,self.count)
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



    def showAnsConfirm(self, ease):
        assert ease<5, "key matrix is mapped for 1-4 only"
        if self.conf.get('show_answer_confirmation',False):
            k=ANS_KEY_MATRIX[self.count-2][ease-1]-1
            msg="%s!<br>"%("Again","Hard","Good","Easy")[k]
            d=self.conf.get('tooltip_duration',1200)
            if self.real_ease:
                btn=self.btns[self.real_ease-5][0]
                msg+=btn+'<br>'
                self.real_ease=0
            # msg+='ivl='+str(mw.reviewer.card.ivl)
            tooltipHint(msg,d/1.5)

