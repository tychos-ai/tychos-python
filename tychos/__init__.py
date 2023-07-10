from .vector_data_store import VectorDataStore
from .vector import _Vector

import os

class Tychos:
    @property
    def api_key(self):
        return os.getenv('TYCHOS_API_KEY')

    @api_key.setter
    def api_key(self, value):
        os.environ['TYCHOS_API_KEY'] = value