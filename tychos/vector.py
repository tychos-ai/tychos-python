import requests

class Vector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://www.tychos.ai/api/'
        # self.base_url = 'http://localhost:3000/api/'
    
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
    