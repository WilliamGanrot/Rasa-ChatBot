from __future__ import print_function

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker, Action, ActionExecutionRejection
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from difflib import SequenceMatcher
import webbrowser

from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

import pickle

import os.path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pprint

"""
DIRECTIONS
"""
class ActionRequestDirections(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        return "directions_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        
        """A list of required slots that the form has to fill"""
        return ["to_location", "from_location", "travel_mode"]

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")
        return []



"""Action form for booking a meeting"""
class ActionRequestVacation(FormAction):

    """Defining the name of the form"""
    def name(self) -> Text:
        return "vacation_form"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["minDate", "maxDate"]
        
    def validate_minDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:
        print("validate_minDate")
        print(tracker.get_slot("time"))
        """        
        if tracker.latest_message['intent'].get('name') == "inform_return_date":
            if type(tracker.get_slot("time")) is dict:
                return { 'maxDate': tracker.get_slot("time")['to'] }
            else:
                if tracker.get_slot("minTime") == tracker.get_slot("maxTime"):
                    return { 'maxDate': tracker.get_slot("time"), "minDate":None } 
                return { 'maxDate': tracker.get_slot("time") } 

        else:
        """  
        if type(tracker.get_slot("time")) is dict:
            return { 'minDate': tracker.get_slot("time")['from'] }
        else:
            return { 'minDate': tracker.get_slot("time") }

    def validate_maxDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:
        print("validate_maxDate")
        print(tracker.get_slot("time"))
        
        """
        if tracker.latest_message['intent'].get('name') == "inform_leaving_date":
            
            if type(tracker.get_slot("time")) is dict:
                return { 'minDate': tracker.get_slot("time")['from'] }
            
            else:
                if tracker.get_slot("minTime") == tracker.get_slot("maxTime"):
                    return { 'minDate': tracker.get_slot("time"), "maxDate":None}
                else:
                    return { 'minDate': tracker.get_slot("time")}
        else:
        
        """
        if type(tracker.get_slot("time")) is dict:
            return { 'maxDate': tracker.get_slot("time")['to'] }
        else:
            return { 'maxDate': tracker.get_slot("time")}


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        print("in slot_mappings")
        return {
            "minDate": [self.from_entity(entity="time")],
            "maxDate": [self.from_entity(entity="time")],
        }

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        dispatcher.utter_message()
        return []


"""Action to confirm that the requested vacation does not conflict with any not allowed dates"""
class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "check_if_valid_dates"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        """Extract and parse the dates from the slots minDate and maxDate"""
        minDate = tracker.get_slot("minDate")
        maxDate = tracker.get_slot("maxDate")
        
        parsedMinDate = parse(minDate)
        parsedMaxDate = parse(maxDate)

        vaild_date_range = False
        """Temporary list of not allowed vacation dates"""
        not_allowed_dates = [datetime(2020, 2, 12, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600))),
                             datetime(2020, 7, 23, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600))),
                             datetime(2020, 3, 9, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600))),
                             datetime(2020, 2, 17, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600)))]


        """Calculate all the dates between minDate and maxDate"""
        delta = parsedMaxDate-parsedMinDate
        between_dates = [parsedMinDate + timedelta(days=i) for i in range(delta.days + 1)]

        """if not any conficts in the date lists allow vacation"""
        if not any(x in not_allowed_dates for x in between_dates):
            vaild_date_range = True

        return [SlotSet("is_valid_dates", vaild_date_range)]
    

"""Action create link to set up meeting"""
class ActionHelloWorld2(Action):

    """Defining the name of the Action"""
    def name(self) -> Text:
        return "book_in_calender"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        """Extract the dates which we want vacation between"""
        minDate = tracker.get_slot("minDate")
        maxDate = tracker.get_slot("maxDate")

        url = "http://ganrot.pythonanywhere.com/test?minDate="+minDate+"&maxDate="+maxDate
        
        dispatcher.utter_message("Okay, go ahead and press this link and I will set it up for you!")
        dispatcher.utter_message(url)
    
        return []


"""Action form for booking meeting"""
class RequestMeeting(FormAction):
    """Example of a custom form action"""

    """Defining the name of the form"""
    def name(self) -> Text:
        return "meeting_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["meeting_date", "inviteemail", "invite_more_bool"]
    
    """Once one or more emails has been extracted by duckling put them in a global email-list"""
    def validate_inviteemail(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:

        new_email_list = ""

        """
        If more than one email was extracted by duckling, loop through them and append them to new_email_list,
        else only one email was extracted and add it to new_email_list
        """
        if type(value) == list:    
            for e in value:
                new_email_list = new_email_list + e + ","
              
        else:
            new_email_list = value + ","

        """Add the new_email_list to the global slot emaillist"""
        if tracker.get_slot("emaillist") == None:
            return {"emaillist": new_email_list}
            
        else:
            return {"emaillist": tracker.get_slot("emaillist") + new_email_list}


    """
    Check if the user want to add more emails to the emaillist,
    If the user want to add more emails, reset the slot inviteemail
    which means that the bot will ask for more email adresses.
    """

    def validate_invite_more_bool(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:

        if tracker.latest_message['intent'].get('name') == "affirm_add_more" or tracker.latest_message['intent'].get('name') == "inform_email":

            emails = [e['additional_info']['value'] for e in tracker.latest_message['entities']]

            new_email_list = ""
            for e in emails:
                new_email_list = new_email_list + e + ","

            return {"emaillist": tracker.get_slot("emaillist") + new_email_list, "inviteemail": tracker.get_slot("email"), "invite_more_bool": None}

        else:

            if value == True:
                return {"invite_more_bool": None, "inviteemail": None}
            else:
                return {"invite_more_bool": value}

    """Define what will fill the form slots"""
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "inviteemail": [
                self.from_entity(entity="email")
            ],
            "meeting_date": [
                self.from_entity(entity="time")
            ],
            "invite_more_bool": [
                self.from_entity(entity="invite_more_bool"),
                
                self.from_intent(intent="affirm_add_more", value=True),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="inform_email", value=True),

                self.from_intent(intent="deny", value=False),
            ]
        }
        
    """
    Once the form is filled prepare a post request to our flask server,
    the server will then generate invitation-links and send to all the users
    """
    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        url = "http://ganrot.pythonanywhere.com/createmeeting"
        
        """Extract all the emails from the slot emaillist and put them in the new list emails"""
        emails = tracker.get_slot("emaillist").split(',')
        for email in emails:
            if not email:
                emails.remove(email)

        """Set up payload for post request to flask server"""
        payload = {
            'meetingDate': str(parse(tracker.get_slot("meeting_date")).date()),
            'email' : emails
        }
        
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(payload)

        """Make post request"""
        request = Request(url, urlencode(payload).encode())
        json = urlopen(request).read().decode()

        dispatcher.utter_message(template="utter_submit")
        return []



class ActionForgotPassword(FormAction):
    def name(self) -> Text:
        return "forgot_password_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["host_email"]

    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List [Dict]]]:
       return {
           "host_email": [
               self.from_entity(entity="email")
           ]
       }

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")
        return []