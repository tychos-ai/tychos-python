import unittest
from tychos import Tychos, VectorDataStore, _Vector
import os
from dotenv import load_dotenv

load_dotenv()

class TestTychos(unittest.TestCase):
    def test_set_api_key(self):
        tychos = Tychos()
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        self.assertEqual(tychos.api_key, os.getenv('USER_TYCHOS_API_KEY'))

    def test_vector_data_store(self):
        tychos = Tychos()
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        vector_data_store = VectorDataStore(api_key=tychos.api_key)
        result = vector_data_store.list()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_vector_data_store_query(self):
        tychos = Tychos()
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        vector_data_store = VectorDataStore(api_key=tychos.api_key)
        result = vector_data_store.query('name', 'query_string', 10)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_vector(self):
        tychos = Tychos()
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        vector = _Vector(api_key=tychos.api_key)
        result = vector.create('text_embedding', 'input_text', 'text-embedding-ada-002')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()
