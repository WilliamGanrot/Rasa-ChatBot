from __future__ import print_function

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from difflib import SequenceMatcher


from datetime import datetime, timedelta
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
        """

        travel_mode = "driving" #Default travel_mode
        highest_score = 0

        modes =	{
            "bicycling": "bicycling",
            "bicycle": "bicycling",
            "bike": "bicycling",
            "biking": "bicycling",
            "car": "driving",
            "drive": "driving",
            "driving": "driving",
            "taxi": "driving",
            "walk": "walking",
            "walking": "walking",
            "foot": "walking",
            "transit": "transit",
            "buss": "transit",
            "train": "transit",
            "subway": "transit",
            "public trainsportation": "transit"
        }

        for x in modes:
            temp_score = SequenceMatcher(None, x, tracker.get_slot("travel_mode")).ratio()
            

            if temp_score > highest_score:
                highest_score = temp_score
                travel_mode = modes[x]




        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return [SlotSet("travel_mode", travel_mode)]
        """
        dispatcher.utter_message(template="utter_submit")
        return []

class ActionRequestVacation(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        return "vacation_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["minDate", "maxDate"]

    def validate_minDate(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        print("setting minDate")
        SlotSet("minDate", tracker.get_slot("time"))

        return {
            'minDate': tracker.get_slot("time")
        }
    def validate_maxDate(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Optional[Text]:

        print("setting maxDate")
        SlotSet("maxDate", tracker.get_slot("time"))
        
        return {
            'maxDate': tracker.get_slot("time")
        }



    def format(self, d):
        return d.isoformat('T')

    def not_allowed_dates(self):
        return [datetime(2020, 2, 12, 0, 0),
                datetime(2020, 7, 23, 0, 0),
                datetime(2020, 1, 9, 0, 0),
                datetime(2020, 2, 17, 0, 0)]

    def get_between_dates(self, maxTime, minTime):
        delta = maxTime - minTime
        between_dates = [minTime + timedelta(days=i) for i in range(delta.days + 1)]
        return between_dates

    def is_date_range_valid(self, not_allowed_dates, between_dates):
        
        #if the date is allowed, check if any intersects in the not_allowed_dates() list and the dates between minTime and maxTime
        if not any(x in not_allowed_dates for x in between_dates):
            return True
        else:
            return False

    def create_event(self, service, minTime, maxTime):
        print("mintime: " + minTime)
        print("maxtime: " + maxTime)

        event = {
        'summary': 'Summary',
        'location': 'Karlstad',
        'description': 'A test event.',
        'start': {
            'dateTime': minTime,
        },
        'end': {
            'dateTime': maxTime,
        }}

        result = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (result.get('htmlLink')))


    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:
        
        print("1")

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
        service = build('calendar', 'v3', credentials=creds)


        print(tracker.get_slot("minDate"))
        print(tracker.get_slot("maxDate"))
        
        maxDate = tracker.get_slot("maxDate")
        minDate = tracker.get_slot("minDate")

        parsedMaxDate = parse(maxDate)
        parsedMinDate = parse(minDate)

        delta = parsedMaxDate - parsedMinDate
        between_dates = [parsedMinDate + timedelta(days=i) for i in range(delta.days + 1)]

        d= self.not_allowed_dates()
        #if the date is allowed, check if
        if self.is_date_range_valid(d, self.get_between_dates(parsedMaxDate, parsedMinDate)):
            print("You can travel")
            self.create_event(service, minDate, maxDate)
        else:
            print("you can not travel")

        dispatcher.utter_message(template="utter_submit")
        return []
