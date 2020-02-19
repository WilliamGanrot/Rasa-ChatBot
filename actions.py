
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from difflib import SequenceMatcher

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

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")
        return []
