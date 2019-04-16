# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/ReMemorizeButtons
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html



from anki import version
ANKI21 = version.startswith("2.1.")

ANS_BTN_TAG='_answerButtonList' if ANKI21 else 'answerButtonList'

ADDON_NAME='rememorize_btn'

DEFAULT_BTN=(('ReM',25),)
