from .vector_data_store import VectorDataStore

class Tychos:
    def __init__(self):
        self.api_key = None
        self.VectorDataStore = VectorDataStore

tychos = Tychos()