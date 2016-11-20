import json
import requests
from urllib import urlencode
from nose.tools import set_trace

class Sierra(object):

    TOKEN_URL = 'https://libcat1.amnh.org/iii/sierra-api/v3/token'
    BIB_URL = 'https://libcat1.amnh.org/iii/sierra-api/v3/bibs/query'

    def __init__(self):
        self.token = None
        self.update_credentials()
        pass

    def update_credentials(self):
        if not self.token:
            data = dict(grant_type='client_credentials')
        response = requests.post(
            self.TOKEN_URL,
            auth=('iPPXbI4/U0udC4T9Q2qjsbTmeIJF', 'hackathon'), data=data
        )
        self.token = response.json().get('access_token')

    def get(self, url, **kwargs):
        bearer = 'Bearer %s' % self.token
        response = requests.get(
            url, headers=dict(Authorization=bearer), **kwargs
        )
        if self.unauthorized_response(response):
            return self.refresh_token(url)
        return response

    def post(self, url, **kwargs):
        bearer = 'Bearer %s' % self.token
        response = requests.post(
            url, headers=dict(Authorization=bearer), **kwargs
        )
        return response

    def refresh_token(self, url):
        self.update_credentials()
        return requests.get(url)

    def unauthorized_response(self, response):
        if (response.status_code == 401 and response.json()['code']==123
            and response.json()['description']=='invalid_grant'):
            return True
        return False

    def search(self, search_text, offset, limit):
        search_text = [word.lower() for word in search_text.split()]
        def title_search(text):
            return {
                "target": {
                    "record": {"type" : "bib"},
                    "field": {"tag" : "t"}
                },
                "expr": {
                    "op": "has",
                    "operands": text
                }
            }

        query = dict(queries=list())
        query['queries'].append(title_search(search_text))
        url = self.BIB_URL + '/query?' + urlencode(dict(offset=offset, limit=limit))
        response = self.post(self.BIB_URL, data=dict(query=query))
        # def subject_search(text):
        #     return {
        #         "target": {
        #             "record": {"type" : "bib"},
        #             "field": {"tag" : "title"}
        #         }
        #     }
        # [
        #     {
        #       "target": {
        #         "record": {"type": "bib"},
        #         "field": {"tag": "t"}
        #       },
        #       "expr": {
        #         "op": "equals",
        #         "operands": ["moby dick"]
        #       }
        #     },
        #     "and",
        #     {
        #       "target": {
        #         "record": {"type": "bib"},
        #         "field": {"tag": "a"}
        #       },
        #       "expr": {
        #         "op": "has",
        #         "operands": ["melville"]
        #       }
        #     }
        #   ]

        pass

    def get_item(self, bib_id):
        pass
