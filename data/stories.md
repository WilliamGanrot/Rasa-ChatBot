<!-- With Hello --->

## happy direction path
* greet
    - utter_greet
* request_directions
    - directions_form
    - form{"name": "directions_form"}
    - form{"name": null}
    - utter_give_directions

## happy direction path 2
* greet
    - utter_greet
* request_directions
    - directions_form
    - form{"name": "directions_form"}
    - form{"name": null}
    - utter_give_directions
* thank_you_bye
    - utter_confirm_thank_you_bye

<!-- No Hello --->

## happy direction path 3
* request_directions
    - directions_form
    - form{"name": "directions_form"}
    - form{"name": null}
    - utter_give_directions

## happy direction path 4
* request_directions
    - directions_form
    - form{"name": "directions_form"}
    - form{"name": null}
    - utter_give_directions
* thank_you_bye
    - utter_confirm_thank_you_bye

<!-- With Hello --->
	
## happy vacation path
* greet
    - utter_greet
* request_vacation
    - utter_ok
    - vacation_form
    - form{"name": "vacation_form"}
    - form{"name": null}
    - utter_date_values
* thank_you_bye
    - utter_confirm_thank_you_bye
	
<!-- No Hello --->

## happy vacation path 2
* request_vacation
    - utter_ok
    - vacation_form
    - form{"name": "vacation_form"}
    - form{"name": null}
    - utter_date_values
    - check_if_valid_dates
        - slot{"is_valid_dates": true}
            - utter_ask_add_to_calender
                * affirm
                    - book_in_calender
* thank_you_bye
    - utter_confirm_thank_you_bye


## happy vacation path 2
* request_vacation
    - utter_ok
    - vacation_form
    - form{"name": "vacation_form"}
    - form{"name": null}
    - utter_date_values
    - check_if_valid_dates
        - slot{"is_valid_dates": true}
            - utter_ask_add_to_calender
                * deny
                    - utter_confirm_thank_you_bye
* thank_you_bye
    - utter_confirm_thank_you_bye



## happy vacation path 2
* request_vacation
    - utter_ok
    - vacation_form
    - form{"name": "vacation_form"}
    - form{"name": null}
    - utter_date_values
    - check_if_valid_dates
        - slot{"is_valid_dates": false}
            - utter_not_valid_dates
* thank_you_bye
    - utter_confirm_thank_you_bye




## happy meeting path
* greet
    - utter_greet
* request_meeting
    - utter_ok
    - meeting_form
    - form{"name": "meeting_form"}
    - form{"name": null}

## happy meeting path 2
* request_meeting
    - utter_ok
    - meeting_form
    - form{"name": "meeting_form"}
    - form{"name": null}




## fallback story
* out_of_scope
    - action_default_fallback 
