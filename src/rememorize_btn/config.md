# ReMemorize Buttons

## enable_write_access
true or false  
Enable the use of modifier buttons.  

In read only mode, this addon requires ReMemorize for scheduling.  Make sure to check the settings for ReMemorize such as sibling forget, sibling reschedule, and fuzz_days.  


## rememorize_buttons:
Add or remove numbers as needed, one number for each extra button will be created.  
Values: positive or negative intervals, positive or negative dates, and zero. No p prefix.  

New interval for each extra button.  
This number is passed to ReMemorize.  
Any fuzz, defuzz, load balancing, or freeweekend stuff will be handled by each respective addon.  


## modifier buttons
Requires "enable_write_access" set to true.  
Add or remove numbers as needed, one number for each extra button will be created.  
This will add extra buttons with custom ease bonus. It will be recorded to the review logs as regular reviews with a grade depending on the new interval.  


## hard_grade_threshold:
integer, best range 60-80% (default 60)  
Modifier buttons are graded according to their next interval. If the adjusted interval falls below this threshold, it'll be graded as "again", but above it, it'll be graded as "hard".  
e.g. The current interval is 10d, threshold would be 6d, if the modifier button is calculated to be 5d, it'll be graded as "again" and the card will lapse. This is similar to setting new lapsed interval modifier as 50%. However if the calculated interval is 6d or 7d, then it'll be within the threshold and graded as "hard".  


## allow_lapse_grade:
true or false  
If the grade falls below 60% of current interval, grade as "again".  


## keep_ease_factor:
true or false  
Modifier buttons are graded according to their next interval. Anki will adjust the ease factor based on this grade. Setting this to true will keep the original factor regardless of the grade.  


## young_card_ivl:
0 to disable.  
Don't show buttons for young cards less than this number.  


## disallow_filtered_decks:
true or false  
Don't show buttons in filter decks (custom study).  

## show_tooltip:
true or false  
Shows a friendly message after reschedule.  

## show_answer_confirmation:
Show tooltip for which button as pressed.  

## cascade_easy_button:
If the 3rd or 4th button is missing, the next lower button number will be used.  

## show_btn_time_in_days:
Decodes 1/25/2019 into days and display them as "25d" in button's next due.  

## button_text_prefix
Friendly reminder text, but you should really use CSS to style and colorize these buttons. Look for a good addon that css styling.  
CSS class: <i>rem_error</i> or <b>rem_timeN</b>, where N is the number of the extra button, 12345...  
e.g.  
rem_time1 {color:red;}  
rem_time1 ~ button{background-color:green;}  
rem_error {color:red;}  
rem_error ~ button{background-color:red;}  

