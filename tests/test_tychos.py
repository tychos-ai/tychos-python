import unittest
from tychos import Tychos
import os
from dotenv import load_dotenv

load_dotenv()

tychos = Tychos()

class TestTychos(unittest.TestCase):
    def test_set_api_key(self):
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        self.assertEqual(tychos.api_key, os.getenv('USER_TYCHOS_API_KEY'))

    def test_vector_data_store(self):
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        print(tychos.vector_data_store)
        result = tychos.vector_data_store.list()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_vector_data_store_query(self):
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        result = tychos.vector_data_store.query('name', 'query_string', 10)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_vector(self):
        tychos.api_key = os.getenv('USER_TYCHOS_API_KEY')
        result = tychos.vector.create('text_embedding', 'input_text', 'text-embedding-ada-002')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

if __name__ == '__main__':
    unittest.main()
