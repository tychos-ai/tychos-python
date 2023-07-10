import requests
import unkey
from . import tychos

class _Vector:
    def __init__(self):
        if tychos.api_key is None:
            raise ValueError("API key not set. Please set the API key using 'tychos.api_key = <your_api_key>'. If you need to create an API key, you can go so at tychos.ai")
        self.api_key = tychos.api_key
        self.base_url = 'https://www.tychos.ai/api/'
        # self.base_url = 'http://localhost:3000/api/'
    
    async def initialize(self):
        await self._verify_api_key()

    async def _verify_api_key(self):
        unkey_client = unkey.Client(api_key=self.api_key)
        await unkey_client.start()
        result = await unkey_client.keys.verify_key(self.api_key)

        if result.is_ok:
            data = result.unwrap()
        else:
            raise ValueError(result.unwrap_err())
        
        await unkey_client.close()
        
    def create(self, type, input_text, model, model_provider_key=None):
        if type == "text_embedding":
            if model == "text-embedding-ada-002":
                try:
                    url = f'{self.base_url}/create-vector'
                    headers = {'api_key': self.api_key}
                    payload = {
                                'model_provider_key': model_provider_key,
                                'input': input_text,
                                'model': model,
                            }
                    response = requests.post(url=url, headers=headers, json=payload)

                    # error handling
                    response.raise_for_status()

                    return response.json()
                except Exception as e:
                    print(e)
                    return None
            else:
                print("Model not currently supported, try text-embedding-ada-002")
                return None
        else:
            print("Type not currently supported, try text_embedding")
            return None
    