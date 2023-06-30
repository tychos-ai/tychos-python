import requests

class VectorDataStore:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://www.tychos.ai/api/'
        # self.base_url = 'http://localhost:3000/api/'

    def query(self, name, query_string, limit):

        # send query request to vector data store
        url = f'{self.base_url}/query-vector-store'
        headers = {'api_key': self.api_key}
        payload = {
                    'name': name,
                    'query_string': query_string,
                    'top': limit,
                }
        response = requests.post(url=url, headers=headers, json=payload)

        # error handling
        response.raise_for_status()

        return response.json()