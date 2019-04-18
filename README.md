# ReMemorize Buttons: Extra buttons for reschedule

## About:
<b>Note:</b> This is not a stand alone addon and requires ReMemorize for scheduling.

This is a graphical front end that sends a signal to ReMemorize and reschedules the current card in the reviewer. Logging, Fuzz, and load balance are performed by ReMemorize.  

The extra buttons are logged as reschedules, as oppose to regular reviews, they are not intended for abuse.  

You can create as many custom buttons as you need.  

Values include: positive or negative intervals, positive or negative dates, and zero. No p prefix.  


## Permissions:
Read Only.  
Standard Read/Write access to config.json file.  


## Hotkeys:
On V1, depending on the card, there may be 4, 3 or even 2 buttons. The good button maybe mapped to 2 or 3 and the easy button mapped to 3 or 4. The shortcuts in this addon is coded to start at the 5th button regardless of how many buttons there may be. You will get a friendly warning if you press button 4 when there is only 3 buttons.


## Conflicts:
This addon will not work with "more answer buttons for new cards". Specifically, that addon will not play well with other button tweek addons. The current and past versions are hardcoded and capped at 3-4 buttons max.


## Colors:
Color can be added with this addon: https://ankiweb.net/shared/info/1829090218  
The stylesheet will need to be tweeked a bit as follows:  
```
/* colorize ReMemorize buttons */
.rem_time1 ~ button {
    background-color: lightgray !important;
}
.rem_time2 ~ button {
    background-color: darkgray !important;
}
.rem_error ~ button {
    background-color: red !important;
}


/* colorize ReMemorize time string */
.rem_time1 {
    color: blue !important;
}
.rem_time2 {
    color: red !important;
}
```

CSS classes:  
<b>rem_error</b> - used to warn of string parsing errors. When it cannot convert string into days or when it is already past due.  
<b>rem_timeN</b> - N is the number of the extra button, 12345...  



## Screenshots:
<img src="https://github.com/lovac42/ReMemorizeButtons/blob/master/screenshots/screen2.png?raw=true">  

<img src="https://github.com/lovac42/ReMemorizeButtons/blob/master/screenshots/screen.png?raw=true">  

