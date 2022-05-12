# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import numpy as np
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from requests.auth import HTTPBasicAuth
import PyPDF2


class ActionSayShirtSize(Action):

    def name(self)  -> Text:
        return "action_say_shirt_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shirt_size = tracker.get_slot("shirt_size")
        if not shirt_size:
            dispatcher.utter_message(text="I dont know your shirt size!")
        else:
            dispatcher.utter_message(text=f"Your shirt size is {shirt_size}!")
        return []

class ActionReceiveName(Action):

    def name(self)  -> Text:
        return "action_receive_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        text = tracker.latest_message['text']
        dispatcher.utter_message(text=f"I'll remember your name {text}")

        return [SlotSet("name", text)]

class ActionSayName(Action):

    def name(self)  -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(text="I  dont know your name.")
        else:
            dispatcher.utter_message(text=f"Your name is  {name}")
        return []

class ActionReadFile(Action):

    def name(self)  -> Text:
        return "action_read_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']

        if text=="textFile":
            f = open('C:\Elfreeda\chatbot.txt','r', errors='ignore')
            raw_doc = f.read()
        elif text=="pdfFile":
            # creating a pdf file object 
            pdfFileObj = open('C:\Elfreeda\chatbot.pdf', 'rb') 
    
            # creating a pdf reader object 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
                
            # printing number of pages in pdf file 
            print(pdfReader.numPages) 
                
            # creating a page object 
            pageObj = pdfReader.getPage(0) 
                
            # extracting text from page 
            print(pageObj.extractText()) 
            raw_doc = pageObj.extractText()
                
            # closing the pdf file object 
            pdfFileObj.close()
        else:
            f = open('C:\Elfreeda\chatbot.txt','r', errors='ignore')
            raw_doc = f.read()
        print("The contents of the document is :\n "+raw_doc)

        # nltk.download('punkt')
        # nltk.download('wordnet')
        # sent_tokens = nltk.sent_tokenize(raw_doc)
        # word_tokens = nltk.word_tokens(raw_doc)

        # lemmer = nltk.stem.WordNetLemmatizer()
        # res_val = user_response('data_science')
        
        # remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

        # def LemTokens(tokens):
        #     return [lemmer.lemmatize(token) for token in tokens]

        # def LemNormalize(text):
        #     return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

        # def user_response(response):
        #     robo1_response=''
        #     TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        #     tfidf = TfidfVec.fit_transform(sent_tokens)
        #     vals = cosine_similarity(tfidf[-1], tfidf)
        #     idx =  vals.argsort()[0][-2]
        #     flat = vals.flatten()
        #     flat.sort()
        #     req_tfidf = flat[-2]
        #     if(req_tfidf == 0):
        #         robo1_response = robo1_response + "I am sorry! I don't undestand you"
        #         return robo1_response
        #     else:
        #         robo1_response = robo1_response+sent_tokens[idx]
        #         return robo1_response

        # text: "Here is your data: \n
        #      - requirement: {requirement}\n
        #      - mockup: {mockup}\n
        #      - url: {url}\n
        #      - timeline: {timeline}\n
        #      - budget: {budget}\n
        #      - name: {name}\n
        #      - email: {email}\n
        #      - phone: {phone}"
        
        dispatcher.utter_message(text=f"I read your file!. Details are : \n {raw_doc}")

        # dispatcher.utter_message(response="utter_file_data", data=raw_doc, phone=phone)
        
        return []

class ActionGetWeatherApiResult(Action):

    def name(self)  -> Text:
        return "action_get_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def Weather(city): 
            api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
            proxies = {
                'http': 'http://proxy.proxy_name.com:9090',
                'https': 'http://proxy.proxy_name.com:9090',
            }
            url = api_address + city 
            json_data = requests.get(url, proxies=proxies).json() 
            format_add = json_data['main'] 
            print(format_add) 
            return format_add


        city = tracker.latest_message['text']
        print("City entered by user is : "+city)
        temp = (Weather(city)['temp']) -273
        temp = round(temp,2)
        dispatcher.utter_message(text=f"the temp is  : {temp} degree Celsius")
        return []

class ActionGetALMApiResult(Action):

    def name(self)  -> Text:
        return "action_get_alm_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def ALMApiCall():
            proxies = {
                'http': 'http://proxy.proxy_name.com:9090',
                'https': 'http://proxy.proxy_name.com:9090',
            }

            alm_url ='url'
            resp_data = requests.get(alm_url,proxies=proxies,  
                                    #auth=HTTPBasicAuth('username', 'password'), 
                                    headers = {'Authorization':'Token generated from the postman using Basic Auth'},
                                    verify=False).json()
            print("Response data is :" + resp_data['items'][0]['pluginName'])
            format_data = resp_data['items']
            return format_data

        slpr_plugins = ALMApiCall()
        dispatcher.utter_message(text="The plugin details are as below: \n")
        for plugin in slpr_plugins:
            dispatcher.utter_message(response="utter_alm_data", pluginName=plugin['pluginName'], pluginType=plugin['pluginType'],pluginVersion=plugin['version'])
        
        return []

class ActionGetJamaApiResult(Action):

    def name(self)  -> Text:
        return "action_get_jama_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        def JamaData():
            proxies = {
                'http': 'http://proxy.proxy_name.com:9090',
                'https': 'http://proxy.proxy_name.com:9090',
            }

            jama_url ='url'
            resp_data = requests.get(jama_url,proxies=proxies, 
                                    #auth=HTTPBasicAuth('username', 'password'), 
                                    headers = {'Authorization':'Token generated from the postman using Basic Auth'},
                                    verify=False).json()
            print("Response data is :" + resp_data['data'][0]['username'])
            format_add = resp_data['data']
            return format_add

        jamaUsers = JamaData()
        dispatcher.utter_message(text="Details of JAMA users are as below: ")
        for user in jamaUsers:
            dispatcher.utter_message(response="utter_jama_data", id=user['id'], username=user['username'], firstName=user['firstName'],
                                    lastName=user['lastName'], email=user['email'], licenseType=user['licenseType'],active=user['active'], type=user['type'])
        
        return []









# ---------------- CODE TO IMPROVISE LATER --------------------------

# class ActionButtonSelect(Action):

#     def name(self) -> Text:
#         return "action_button_selection"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         button_resp=[
#                     {
#                         "title": "txtFile",
#                         "payload": "txtFile"
#                     },
#                     {
#                         "title": "pdfFile",
#                         "payload": "pdfFile"
#                     }
#                 ]

#         dispatcher.utter_message(text="Select a file to read", buttons=button_resp)

#         return []

# class ActionInlineLink(Action):

#     def name(self) -> Text:
#         return "action_inline_link"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         link_resp=[
#                     {
#                         "inline": "ALM Dev Home",
#                         "url": "https://alm.rockwellcollins.com/wiki/display/ALMDEVW"
#                     }
#                 ]

#         dispatcher.utter_message(text="Here is your url to access", link=link_resp)

#         return []
