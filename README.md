# ReMemorize Buttons: Extra buttons for reschedule

## About:
<b>Note:</b> In read only mode, this addon requires ReMemorize for scheduling.

### ReMemorize Buttons:
In read only mode, this addon sends a signal to ReMemorize and reschedules the current card in the reviewer. Logging, Fuzz, and load balance are performed by ReMemorize. The ReMemorize buttons are logged as reschedules, not as regular reviews, they are not intended for abuse. Use the modifier buttons if you need these logged as regular reviews.

Values include: positive or negative intervals, positive or negative dates, and zero. No p prefix.  

You can remove or create as many custom buttons as you need.  


### Modifier Buttons:
In write enabled mode, modifier buttons are created. These buttons are used similar to the interval modifier and are logged as regular reviews. If the adjusted interval is above the good button, it will be counted as an ease bonus and graded as "easy" 4. If below good, it'll be graded as "good" 3. And below a certain threshold, it's graded as "hard" 2. Below this threshold, it's counted as "again" 1 or lapsed.

You can remove or create as many custom modifier buttons as you need.  



## Hotkeys:
On V1, depending on the card, there may be 4, 3 or even 2 buttons. The good button maybe mapped to 2 or 3 and the easy button mapped to 3 or 4. The shortcuts in this addon is coded to start at the 5th button regardless of how many buttons there may be. You will get a friendly warning if you press button 4 when there is only 3 buttons. In config option, enable "cascade_easy_button" to redirect this phantom button to the actual easy button.


## Conflicts:
This addon will not work with "more answer buttons for new cards".


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
<b>rem_reschedule</b> - ReMemorize buttons.  
<b>rem_modifier</b> - custom modifier buttons.  



## Screenshots:
<img src="https://github.com/lovac42/ReMemorizeButtons/blob/master/screenshots/screen2.png?raw=true">  

<img src="https://github.com/lovac42/ReMemorizeButtons/blob/master/screenshots/screen.png?raw=true">  

<img src="https://github.com/lovac42/ReMemorizeButtons/blob/master/screenshots/donts.png?raw=true">  

<img src="https://github.com/lovac42/ReMemorizeButtons/blob/master/screenshots/logs.png?raw=true">  

