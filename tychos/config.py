class TychosConfig:
    def __init__(self):
        self._api_key = None

    def __get__(self, instance, owner):
        return self._api_key

    def __set__(self, instance, value):
        self._api_key = value