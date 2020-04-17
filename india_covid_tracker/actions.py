# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionStatewiseTracker(Action):

    def name(self) -> Text:
        return "action_covid_statewise_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get('https://api.covid19india.org/data.json').json()
        # print(response)
        # print(tracker.latest_message)
        entities =  tracker.latest_message['entities']
        print("Latest Message : ", entities)

        state = None
        for e in entities:
            if e['entity'] == 'state':
                state = e['value']
            for data in response['statewise']:
                if data['state'] == state.title():
                    print("Data is : ",data)
                    # {'active': '45', 'confirmed': '83', 'deaths': '1', 'deltaconfirmed': '11', 'deltadeaths': '0', 'deltarecovered': '8', 
                    # 'lastupdatedtime': '16/04/2020 23:13:07', 'recovered': '37', 'state': 'Bihar', 'statecode': 'BR', 'statenotes': ''}
                    message = "Active : " + data['active'] + \
                              " Confirmed : " + data['confirmed'] + \
                              " Recovered : " + data['recovered'] + \
                              " Deaths : "+ data['deaths'] + \
                              " Last Updated : " + data['lastupdatedtime'] + \
                              " State : " + data['state']

        dispatcher.utter_message(text="Covid Tracker Update : " + message)

        return []
