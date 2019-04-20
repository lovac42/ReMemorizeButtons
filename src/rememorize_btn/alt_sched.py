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
        return 1


    def getBtnIvl(self, card, maxEase):
        e=min(3,max(2,maxEase-1)) #find the good btn
        nxIvl=self.nextRevIvl(card,e)
        return max(1,int(nxIvl*self.modifier))


    # Unreliable results due to _constrainedIvl() by hard ivl.
    # Interval modifier is factored in afterwards. When set to random
    # ivl modifier, the 130% on easy button is different from the 130%
    # used by this addon's modifier buttons.
    def nextRevIvl(self, card, ease, fuzz=False):
        if mw.col.sched.name=="std": #V1
            return mw.col.sched._nextRevIvl(card,ease)
        else: #V2
            return mw.col.sched._nextRevIvl(card,ease,fuzz)


    def hasSavedIvl(self):
        return self.meta_card.ivl


    def isReschedulable(self, card):
        if not self.conf.get('enable_write_access',False):
            return False

        #check V1 V2 filter reschedule
        if mw.col.sched.name=="std":
            return mw.col.sched._resched(card)
        return True


    def reschedule(self, card, ease, modifier):
        assert self.conf.get('enable_write_access',False)

        self.meta_card.setFactor(card.factor)

        self.setModifier(modifier)
        self.answerCard(card,ease)
        self.reset()


    def answerCard(self, card, ease):
        assert self.isReschedulable(card)
        nxIvl=card.ivl or 1

        if card.queue in (1,3):
            #adds bonus to lrn card's ivl
            nxIvl=max(1,int(nxIvl*self.modifier))
            #Causes Undo problems if manipulating card.ivl directly

        elif card.queue==2:
            nxIvl=self.getBtnIvl(card,ease)
            ease=self.remapBtnGrade(card,nxIvl)

        self.meta_card.setIvl(nxIvl)
        mw.col.sched.answerCard(card,ease)

