import os
import requests
from .vector import _Vector
from .helpers.validation_checks import validate_query_filter

class VectorDataStore:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('TYCHOS_API_KEY')
        self.base_url = 'https://api.tychos.ai/'
        self.vector = _Vector(api_key=self.api_key)

    def query(self, name, query_string, limit, query_filter=None):
        if self.api_key is None:
            raise ValueError("API key not set. Please set the API key using 'tychos.api_key = <your_api_key>'. If you need to create an API key, you can go so at tychos.ai")
        # vectorize query string
        query_vector = self.vector.create(
            type="text_embedding",
            input_text=query_string,
            model="text-embedding-ada-002"
        )

        # validate index name
        available_indices = ['pub-med-abstracts', 'arxiv-abstracts', 'us-patents', 'biorxiv', 'medrxiv']
        if not isinstance(name, list):
            name = [name]
        invalid_names = [n for n in name if n not in available_indices]
        if invalid_names:
            raise ValueError(f"Invalid index name(s): {', '.join(invalid_names)}. The current available datasets are: {', '.join(available_indices)}")
        
        # send query request to vector data store
        url = f'{self.base_url}v1/vector_data_store/query'
        headers = {'api_key': self.api_key}
        payload = {
                    'name': name,
                    'query_vector': query_vector,
                    'top': limit,
                }
        if query_filter is not None:
            validate_query_filter(query_filter)
            payload['query_filter'] = query_filter
        response = requests.post(url=url, headers=headers, json=payload)

        # error handling
        response.raise_for_status()

        return response.json()
    
    def list(self):
        if self.api_key is None:
            raise ValueError("API key not set. Please set the API key using 'tychos.api_key = <your_api_key>'. If you need to create an API key, you can go so at tychos.ai")
        url = f'{self.base_url}v1/vector_data_store/list'
        headers = {'api_key': self.api_key}
        response = requests.get(url=url, headers=headers)

        # error handling
        response.raise_for_status()

        return response.json()