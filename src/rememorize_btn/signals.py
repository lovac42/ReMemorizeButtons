# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.utils import showInfo
from anki.hooks import runHook
from anki.utils import fmtTimeSpan
from .const import *
from .utils import *


class ReMemorizeScheduler:
    def __init__(self, conf):
        self.conf=conf
        self.btns=None

    def setButtons(self, b):
        self.btns=b


    def reschedule(self, card, ease):
        assert ease>4
        due=card.due #save

        days=self._parseDays(ease)
        if days==None:
            return self._parseWarning()

        elif days=='-0':
            return showInfo("PC LOAD A4!")

        elif days=='0':
            runHook('ReMemorize.forget', card)

        elif days>0:
            runHook('ReMemorize.reschedule', card, days)

        elif days<0:
            runHook('ReMemorize.changeDue', card, -days)

        else: return

        self._showTooltip(card,ease,due)


    def getTimeString(self, ease):
        assert ease>4
        if self.conf.get("show_btn_time_in_days",False):
            d=self._parseDays(ease)
            if not d:
                #tobe colorize red with css
                return '<span class="nobold rem_error">ERROR!</span><br>'
            s=fmtTimeSpan(d*86400,short=True)
        else:
            s=self.btns[ease-5][1] #zero based

        p=self.conf.get("button_text_prefix","R: ")
        return '<span class="nobold rem_reschedule rem_time%d">%s%s</span><br>'%(ease-4,p,s)


    def _parseDays(self, ease):
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



    def _showTooltip(self, card, ease, due):
        if self.conf.get('show_tooltip',True):
            d=self.conf.get('tooltip_duration',1200)
            btn=self.btns[ease-5][0]
            mw.progress.timer(20,
                lambda:schedConfirm(card.id,card.ivl,due,d,btn),False)


    def _parseWarning(self):
        showInfo("""
Past due or invalid parsing string,<br>
The reviewer will drop this card,<br>
but you will see it again when it<br>
comes back around. NO CHANGES HAS BEEN MADE.
""")


