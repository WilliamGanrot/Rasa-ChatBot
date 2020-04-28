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
    - check_if_valid_dates
        - slot{"is_valid_dates": true}
            - utter_ask_add_to_calender
                * affirm
                    - book_in_calender
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


## happy vacation path 3
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



## happy vacation path 4
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

## happy forgot password path
* greet
    - utter_greet
* forgot_password
    - forgot_password_form
    - form{"name": "forgot_password_form"}
    - form{"name": null}
    - utter_resend_password
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy forgot password path 2
* greet
    - utter_greet
* forgot_password
    - forgot_password_form
    - form{"name": "forgot_password_form"}
    - form{"name": null}
    - utter_resend_password

## happy forgot password path 3
* forgot_password
    - forgot_password_form
    - form{"name": "forgot_password_form"}
    - form{"name": null}
    - utter_resend_password
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy forgot password path 4
* forgot_password
    - forgot_password_form
    - form{"name": "forgot_password_form"}
    - form{"name": null}
    - utter_resend_password

## happy opening hours path
* greet
    - utter_greet
* ask_opening_hours
    - utter_give_opening_hours
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy opening hours path 2
* greet
    - utter_greet
* ask_opening_hours
    - utter_give_opening_hours

## happy opening hours path 3
* ask_opening_hours
    - utter_give_opening_hours
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy opening hours path 4
* ask_opening_hours
    - utter_give_opening_hours

## happy ask website path
* greet
    - utter_greet
* ask_website
    - utter_give_website
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy ask website path 2
* greet
    - utter_greet
* ask_website
    - utter_give_website

## happy ask website path 3
* ask_website
    - utter_give_website
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy ask website path 4
* ask_website
    - utter_give_website

## happy ask job path
* greet
    - utter_greet
* ask_job
    - utter_give_job_page
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy ask job path 2
* greet
    - utter_greet
* ask_job
    - utter_give_job_page

## happy ask job path 3
* ask_job
    - utter_give_job_page
* thank_you_bye
    - utter_confirm_thank_you_bye

## happy ask job path 4
* ask_job
    - utter_give_job_page

## fallback story
* out_of_scope
    - action_default_fallback 
