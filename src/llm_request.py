from src.payload import Payload

class LLMRequest:
    def __init__(self, payload, from_module, to_module):
        self._type = from_module
        self._to_module = to_module
        self._payload = payload


    def get_type(self):
        return self._type


    def get_to_module(self):
        return self._to_module


    def get_payload(self):
        return self._payload


    def set_type(self, new_type):
        self._type = new_type


    def set_payload(self, payload):
        self._payload = payload