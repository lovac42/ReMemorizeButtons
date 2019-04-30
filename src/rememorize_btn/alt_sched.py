# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from .card import *
from .const import *


class AltScheduler:
    def __init__(self, conf):
        self.conf=conf
        self.meta_card=MetaCard(conf)
        self.modifier=0


    def reset(self):
        self.modifier=0
        self.meta_card.reset()


    def getModifier(self):
        return self.modifier

    def setModifier(self, mod):
        self.modifier=mod


    def remapBtnGrade(self, card, nxIvl):
        for e in (4,3,2):
            if nxIvl>self.nextRevIvl(card,e):
                return min(4,e+1)

        th=self.conf.get('hard_grade_threshold',60)/100.0
        if nxIvl>=int(card.ivl*th):
            return 2

        if self.conf.get('allow_lapse_grade',True):
            return 1
        return 2



    def getBtnIvl(self, card, maxEase):
        e=min(3,max(2,maxEase-1)) #find the good btn
        nxIvl=self.nextRevIvl(card,e)
        return max(1,int(nxIvl*self.modifier))


    def getLrnBtnIvl(self, card, ease):
        nxIvl=mw.col.sched._nextLrnIvl(card,ease) #time string
        return max(1,int(nxIvl*self.modifier)//86400) #extra work for precision


    # Unreliable results due to _constrainedIvl() by hard ivl.
    # Interval modifier is factored in afterwards. When set with an
    # ivl modifier less than 100%, the 130% on the easy button is
    # different from the 130% used by this addon's modifier buttons.
    def nextRevIvl(self, card, ease, fuzz=False):
        if mw.col.sched.name=="std": #V1
            return mw.col.sched._nextRevIvl(card,ease) #no fuzz on V1
        return mw.col.sched._nextRevIvl(card,ease,fuzz) #V2


    def hasSavedFactor(self):
        if not self.conf.get('keep_ease_factor',False):
            return False
        return self.meta_card.getFactor()

    def hasSavedIvl(self):
        if not self.conf.get('enable_write_access',False):
            return False
        return self.meta_card.getIvl()


    def isReschedulable(self, card):
        if not self.conf.get('enable_write_access',False):
            return False
        return self.isDynReschedulable(card)


    def isDynReschedulable(self, card):
        "check V1 V2 filter reschedule"
        dconf=mw.col.sched._cardConf(card)
        if not dconf['dyn']:
            return True
        return dconf['resched']


    def reschedule(self, card, ease, modifier):
        assert self.isReschedulable(card)
        self.setModifier(modifier)
        self._answerCard(card,ease)
        self.reset()


    def _answerCard(self, card, ease):
        #Causes Undo problems if manipulating card.ivl directly

        if card.queue in (0,1,3):
            nxIvl=self.getLrnBtnIvl(card,ease)
        elif card.queue==2:
            self.meta_card.setFactor(card.factor)
            nxIvl=self.getBtnIvl(card,ease)
            ease=self.remapBtnGrade(card,nxIvl)
        else: #queue 4 (preview)
            nxIvl=0 #skip

        self.meta_card.setIvl(nxIvl)
        mw.col.sched.answerCard(card,ease)
