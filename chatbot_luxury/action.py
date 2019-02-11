from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet


class Actionnews(Action):
    
    
    def name(self):
        return 'action_news'
            
    def run(self, dispatcher, tracker, domain):
        from elasticsearch import Elasticsearch

        import json
        import requests

        uri = " "
        loc = tracker.get_slot('market')

        search_word = "Market_" + loc.capitalize()
        
        q = {
            "size" : 5,
            "query" : {
                "bool" : {
                    "must": [
                        { "term" : {"plainTags" : search_word}
                          }
                        ]
                    }
                }
            }

        query = json.dumps(q)
        response = requests.post(uri,query)
        result = json.loads(response.text)
        data = [doc for doc in result['hits']['hits']]

        url_list = []
        for d in data:
            try:
                url_list.append(d['_source']['url'])
            except:
                pass
        if url_list:
            for i in range(len(url_list)):
                if i == 0:
                    r = "News of {} market are {}".format(loc,url_list[i])
                    dispatcher.utter_message(r)
                else:
                    r = "{}".format(url_list[i])
                    dispatcher.utter_message(r)
        else:
            r = "Sorry, No news currently available"
            dispatcher.utter_message(r)
        return [SlotSet('market',loc)]

