# ReMemorize Buttons
This is not a stand alone addon and requires ReMemorize for scheduling.


## buttons:
Add or remove numbers as needed, one number for each extra button will be created.  
Values: positive or negative intervals, positive or negative dates, and zero. No p prefix.  

New interval for each extra button.  
This number is passed to ReMemorize.  
Any fuzz, defuzz, load balancing, or freeweekend stuff will be handled by each respective addon.  


## young_card_ivl:
0 to disable, 31 days max.  
Don't show buttons for young cards less than this number.  
As the reviews are logged as reschedules, you should not abuse this feature.  
Setting it to a small value is acceptable.  

## disallow_filtered_decks:
true or false  
Don't show buttons in filter decks (custom study).  

## show_tooltip:
true or false  
Shows a friendly message after reschedule.  
