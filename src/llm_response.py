class LLMResponse:
    def __init__(self, to_module, response):
        self._to_module = to_module
        self._response = response

    def get_to_module(self):
        return self._to_module

    def get_response(self):
        return self._response