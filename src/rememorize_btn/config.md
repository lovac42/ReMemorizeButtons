# ReMemorize Buttons
This is not a stand alone addon and requires ReMemorize for scheduling.


## buttons:
Add or remove numbers as needed, one number for each extra button will be created.  
Values: positive or negative intervals, positive or negative dates, and zero. No p prefix.  

New interval for each extra button.  
This number is passed to ReMemorize.  
Any fuzz, defuzz, load balancing, or freeweekend stuff will be handled by each respective addon.  


## young_card_ivl:
0 to disable.  
Don't show buttons for young cards less than this number.  
As the reviews are logged as reschedules, you should not abuse this feature.  
Setting it to a small value is acceptable.  

## disallow_filtered_decks:
true or false  
Don't show buttons in filter decks (custom study).  

## show_tooltip:
true or false  
Shows a friendly message after reschedule.  

## show_btn_time_in_days:
Decodes 1/25/2019 into days and display them as "25d" in button's next due.

## button_text_prefix
Friendly reminder text, but you should really use CSS to style and colorize these buttons. Look for a good addon that css styling.  
CSS class: <b>rem_timeN</b>, where N is the number of the extra button, 12345...  
e.g.  
rem_time1 {color:red;}  
rem_time1 ~ button{background-color:green;}  

