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
        indian_states = {"MH":"Maharashtra", "DL":"Delhi", "TN":"Tamil Nadu", "RJ":"Rajasthan", "MP":"Madhya Pradesh", "GJ":"Gujarat", "UP":"Uttar Pradesh", \
            "TG":"Telangana", "AP":"Andhra Pradesh", "KL":"Kerala", "JK":"Jammu and Kashmir", "KA":"Karnataka", "WB":"West Bengal", "HR":"Haryana", \
			"PB":"Punjab", "BR":"Bihar", "OR":"Odisha", "UT":"Uttarakhand", "HP":"Himachal Pradesh", "CT":"Chhattisgarh", "AS":"Assam", "JH":"Jharkhand", \
			"CH":"Chandigarh", "LA":"Ladakh", "AN":"Andaman and Nicobar Islands", "GA":"Goa", "PY":"Puducherry", "ML":"Meghalaya", "MN":"Manipur", \
            "TR":"Tripura", "MZ":"Mizoram", "AR":"Arunachal Pradesh", "DN":"Dadra and Nagar Haveli", "NL":"Nagaland", \
            "DD":"Daman and Diu", "LD":"Lakshadweep", "TT":"Total"}
        state = None
        for e in entities:
            # import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if (e['entity'] == 'state') and len(e['value']) > 2:
                state = e['value']
            else:
                state = indian_states[e['value'].upper()]

            message = "The state " + state + " Not found!!, Please enter correct state name."
            if state == 'india':
                state = 'Total'
            for data in response['statewise']:
                if data['state'] == state.title():
                    print("Data is : ",data)
                    message = "Confirmed : " + data['confirmed'] + \
                              " Active : " + data['active'] + \
                              " Recovered : " + data['recovered'] + \
                              " Deaths : "+ data['deaths'] + \
                              " Last Updated : " + data['lastupdatedtime'] + \
                              " State : " + data['state']

        dispatcher.utter_message(text="Covid Tracker Update : " + message)

        return []
