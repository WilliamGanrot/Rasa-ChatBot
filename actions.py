from __future__ import print_function

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker, Action
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

        dispatcher.utter_message(template="utter_submit")
        return []





class ActionRequestVacation(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        return "vacation_form"
    
    def validate_minDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:

        print("setting minDate")
        SlotSet("minDate", tracker.get_slot("time"))

        return { 'minDate': tracker.get_slot("time") }

    def validate_maxDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:

        print("setting maxDate")
        SlotSet("maxDate", tracker.get_slot("time"))
        
        return { 'maxDate': tracker.get_slot("time") }



    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["minDate", "maxDate"]




    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:


        dispatcher.utter_message()
        return []



"""
class ActionRequestVacation(FormAction):

    def name(self) -> Text:
        return "vacation_form"
    
    def validate_minDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:

        print("setting minDate")
        SlotSet("minDate", tracker.get_slot("time"))

        return { 'minDate': tracker.get_slot("time") }

    def validate_maxDate(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Optional[Text]:

        print("setting maxDate")
        SlotSet("maxDate", tracker.get_slot("time"))
        
        return { 'maxDate': tracker.get_slot("time") }

    def authenticate(self):
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
        return service

    def get_between_dates(self, maxTime, minTime):
        delta = maxTime - minTime
        between_dates = [minTime + timedelta(days=i) for i in range(delta.days + 1)]
        return between_dates

        
    def create_event(self, service, minTime, maxTime):

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
        return result

    def format(self, d):
        return d.isoformat('T')


    def not_allowed_dates(self):
        return [datetime(2020, 2, 12, 0, 0),
                datetime(2020, 7, 23, 0, 0),
                datetime(2020, 1, 9, 0, 0),
                datetime(2020, 2, 17, 0, 0)]

    @staticmethod
    def test(self):
        return True
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        #A list of required slots that the form has to fill
        
        print("X")
        minDate = tracker.get_slot("minDate")
        maxDate = tracker.get_slot("maxDate")


        try:
            parsedMinDate = parse(minDate)
            parsedMaxDate = parse(maxDate)
            
            print("--minDate: " + minDate)
            print("--maxDate:" + maxDate )


            vaild_date_range = False
            not_allowed_dates = [datetime(2020, 2, 12, 0, 0),
                                 datetime(2020, 7, 23, 0, 0),
                                 datetime(2020, 1, 9, 0, 0),
                                 datetime(2020, 2, 17, 0, 0)]

            delta = parsedMaxDate-parsedMinDate
            between_dates = [parsedMinDate + timedelta(days=i) for i in range(delta.days + 1)]

            #if not any conficts in the date lists
            if not any(x in not_allowed_dates for x in between_dates):
                vaild_date_range = True

            if vaild_date_range:
                print("add add_to_calender to required slots")
                return ["minDate", "maxDate", "add_to_calender"]
            
        except:
            pass

        return ["minDate", "maxDate"]



    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return{
            "add_to_calender": [
            self.from_entity(entity="add_to_calender"),
            self.from_intent(intent="affirm", value=True),
            self.from_intent(intent="deny", value=False),
        ]
        }


    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:
        service = self.authenticate()


        print(tracker.get_slot("minDate"))
        print(tracker.get_slot("maxDate"))
        
        maxDate = tracker.get_slot("maxDate")
        minDate = tracker.get_slot("minDate")

        parsedMaxDate = parse(maxDate)
        parsedMinDate = parse(minDate)

        delta = parsedMaxDate - parsedMinDate
        between_dates = [parsedMinDate + timedelta(days=i) for i in range(delta.days + 1)]

        msg = None
        
        #if the date is allowed, check if
        if self.is_date_range_valid(self.not_allowed_dates(), self.get_between_dates(parsedMaxDate, parsedMinDate)):
            print("You can travel")
            result = self.create_event(service, minDate, maxDate)
            msg = "The event has been added to you calender.\nYou can view it here: " + (result.get('htmlLink'))
        else:
            print("you can not travel")
            msg = "You can not travel"

        dispatcher.utter_message(msg)
        return []

"""

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "check_if_valid_dates"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        return [SlotSet("is_valid_dates", False)]