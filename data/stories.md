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

## fallback story
* out_of_scope
    - action_default_fallback 