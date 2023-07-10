import requests
import unkey
import asyncio
from .vector import _Vector
from . import tychos

class VectorDataStore:
    def __init__(self):
        if tychos.api_key is None:
            raise ValueError("API key not set. Please set the API key using 'tychos.api_key = <your_api_key>'. If you need to create an API key, you can go so at tychos.ai")
        self.api_key = tychos.api_key
        self.base_url = 'https://www.tychos.ai/api/'
        # self.base_url = 'http://localhost:3000/api/'
        self.start()

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.initialize())
    
    async def initialize(self):
        await self._verify_api_key()
        self.vector = _Vector()
        await self.vector.initialize()
    
    async def _verify_api_key(self):
        unkey_client = unkey.Client(api_key=self.api_key)
        await unkey_client.start()
        result = await unkey_client.keys.verify_key(self.api_key)

        if result.is_ok:
            data = result.unwrap()
        else:
            raise ValueError(result.unwrap_err())
        
        await unkey_client.close()

    def query(self, name, query_string, limit):
        # vectorize query string
        query_vector = self.vector.create(
            type="text_embedding",
            input_text=query_string,
            model="text-embedding-ada-002"
        )

        # send query request to vector data store
        url = f'{self.base_url}/query-vector-store'
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
        url = f'{self.base_url}/datasets'
        headers = {'api_key': self.api_key}
        response = requests.get(url=url, headers=headers)

        # error handling
        response.raise_for_status()

        return response.json()