import os
import requests
from .vector import _Vector

class VectorDataStore:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('TYCHOS_API_KEY')
        self.base_url = 'https://api.tychos.ai/v1/'
        self.vector = _Vector(api_key=self.api_key)

    def query(self, name, query_string, limit):
        if self.api_key is None:
            raise ValueError("API key not set. Please set the API key using 'tychos.api_key = <your_api_key>'. If you need to create an API key, you can go so at tychos.ai")
        # vectorize query string
        query_vector = self.vector.create(
            type="text_embedding",
            input_text=query_string,
            model="text-embedding-ada-002"
        )

        # send query request to vector data store
        url = f'{self.base_url}vector_data_store/query'
        headers = {'api_key': self.api_key}
        payload = {
                    'name': name,
                    'query_vector': query_vector,
                    'top': limit,
                }
        response = requests.post(url=url, headers=headers, json=payload)

        # error handling
        response.raise_for_status()

        return response.json()
    
    def list(self):
        if self.api_key is None:
            raise ValueError("API key not set. Please set the API key using 'tychos.api_key = <your_api_key>'. If you need to create an API key, you can go so at tychos.ai")
        url = f'{self.base_url}vector_data_store/list'
        headers = {'api_key': self.api_key}
        response = requests.get(url=url, headers=headers)

        # error handling
        response.raise_for_status()

        return response.json()