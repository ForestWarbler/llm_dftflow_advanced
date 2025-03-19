from src.llm_request import LLMRequest
from src.llm_response import LLMResponse
import json


class LLMMessageHandler:
    def __init__(self, response):
        self._response = response


    def handle_message(self):
        to_module = self._response.get_to_module()
        print(self._response.get_response())
        # match to_module:
        #     case '': pass

