from __future__ import print_function

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker, Action, ActionExecutionRejection
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from difflib import SequenceMatcher


from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
import pickle
from dateutil.parser import parse
import os.path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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


class ActionRequestVacation(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        return "vacation_form"

    """    
    def validate_minDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:

        print("setting minDate")

        if type(tracker.get_slot("time")) is dict:
            SlotSet("minDate", tracker.get_slot("time")['from'])
            return { 'minDate': tracker.get_slot("time")['from'] }
        else:
            SlotSet("minDate", tracker.get_slot("time"))
            return { 'minDate': tracker.get_slot("time") }

    def validate_maxDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:

        print("setting maxDate")

        if type(tracker.get_slot("time")) is dict:
            SlotSet("maxDate", tracker.get_slot("time")['to'])
            return { 'maxDate': tracker.get_slot("time")['to'] }
        else:
            SlotSet("maxDate", tracker.get_slot("time"))
            return { 'maxDate': tracker.get_slot("time") }
    """



    def validate(self, dispatcher, tracker, domain):

        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot("requested_slot")
        
        # Validate the time slots
        if type(tracker.get_slot("time")) is dict:

            SlotSet("maxDate", tracker.get_slot("time")['to'])
            SlotSet("minDate", tracker.get_slot("time")['from'])
            slot_values.update({ 'maxDate': tracker.get_slot("time")['to']})
            slot_values.update({ 'minDate': tracker.get_slot("time")['from']})
        else:   
            if slot_to_fill == "maxDate":
                if tracker.get_slot("time") is None:
                    dispatcher.utter_message("I'm sorry I didn't get that.")
                    return []
                print("maxdate provided")
                slot_values.update({ 'maxDate': tracker.get_slot("time")})
            
            elif slot_to_fill == "minDate":
                if tracker.get_slot("time") is None:
                    dispatcher.utter_message("I'm sorry I didn't get that.")
                    return []
                print("mindate provided")
                slot_values.update({ 'minDate': tracker.get_slot("time")})

        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))

            if not slot_values:
                
                raise ActionExecutionRejection(
                    self.name(),
                    "Failed to extract slot {0} "
                    "with action {1}"
                    "".format(slot_to_fill, self.name()),
                )

        return self.validate_slots(slot_values, dispatcher, tracker, domain)

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["minDate", "maxDate"]




    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        print(tracker.get_slot("time"))
        dispatcher.utter_message()
        return []


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "check_if_valid_dates"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_id.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)



        minDate = tracker.get_slot("minDate")
        maxDate = tracker.get_slot("maxDate")
        
        parsedMinDate = parse(minDate)
        parsedMaxDate = parse(maxDate)

        vaild_date_range = False
        not_allowed_dates = [datetime(2020, 2, 12, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600))),
                             datetime(2020, 7, 23, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600))),
                             datetime(2020, 3, 9, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600))),
                             datetime(2020, 2, 17, 0, 0 ,tzinfo=timezone(timedelta(days=0, seconds=3600)))]


        delta = parsedMaxDate-parsedMinDate

        #between_dates = [parsedMinDate + timedelta(days=i) for i in range(delta.days + 1)]
        between_dates = [parsedMinDate + timedelta(days=i) for i in range(delta.days + 1)]

        #if not any conficts in the date lists
        if not any(x in not_allowed_dates for x in between_dates):
            vaild_date_range = True

        return [SlotSet("is_valid_dates", vaild_date_range)]
    


class ActionHelloWorld2(Action):

    def name(self) -> Text:
        return "book_in_calender"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_id.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

        minDate = tracker.get_slot("minDate")
        maxDate = tracker.get_slot("maxDate")

        event = {
        'summary': 'Summary',
        'location': 'Karlstad',
        'description': 'A test event.',
        'start': {
            'dateTime': minDate,
        },
        'end': {
            'dateTime': maxDate,
        }}

        result = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (result.get('htmlLink')))

        dispatcher.utter_message("Okay, I have booked it in you calender, view it here: " + (result.get('htmlLink')))
        return []