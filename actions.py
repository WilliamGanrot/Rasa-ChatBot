
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


class ActionRequestDirections(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        return "directions_form"


    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["to_location", "from_location", "travel_mode"]

    """
    def validate_to_location(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:
        print("AHAHAH this failed AHAHAH")
        #dispatcher.utter_message(template="utter_submit")
    """

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return []