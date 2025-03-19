from llm_request import LLMRequest
from llm_response import LLMResponse
import json


class LLMMessageHandler:
    def __init__(self, response):
        self._response = response


    def handle_message(self, message):
        to_module = self._response.get_to_module()
        match to_module:
            case "": pass

