# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from .const import *


class MetaCard:
    def __init__(self, conf):
        self.conf=conf
        self.reset()

    def reset(self):
        self.ivl=0
        self.factor=0



    def setFactor(self, fct):
        self.factor=fct

    def getFactor(self):
        return self.factor



    def setIvl(self, ivl):
        self.ivl=ivl

    def getIvl(self):
        return self.ivl

