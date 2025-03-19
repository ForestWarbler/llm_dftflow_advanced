from payload import *
from llm_request import *
from llm_request_queue import *
from llm_response import *
from llm_communicator import *
from llm_message_handler import *

class LLMModule:
    def __init__(self, queue_op_num = 5, url = None, model = None, temperature = 0, top_p = 1, max_tokens = 128000, stream = False):
        self._queue_op_num = queue_op_num
        self._url = url
        self._model = model
        self._temperature = temperature
        self._top_p = top_p
        self._max_tokens = max_tokens
        self._stream = stream
        self._llm_request_queue = None
        self._llm_communicator = None
        self._llm_message_handler = None


    def check_queue_op_num(self):
        return self._queue_op_num >= 1


    def check_url(self):
        return self._url is not None


    def check_model(self):
        return self._model is not None


    def check_llm_request_queue(self):
        return self._llm_request_queue is not None


    def check_llm_communicator(self):
        return self._llm_communicator is not None


    def check_llm_message_handler(self):
        return self._llm_message_handler is not None


    def check_all(self):
        return self.check_queue_op_num() and self.check_url and self.check_model() \
           and self.check_llm_request_queue() and self.check_llm_communicator() \
           and self.check_llm_message_handler()


    def set_queue_op_num(self, new_queue_op_num):
        self._queue_op_num = new_queue_op_num


    def set_url(self, new_url):
        self._url = new_url


    def set_model(self, new_model):
        self._model = new_model


    def set_temperature(self, new_temperature):
        self._temperature = new_temperature


    def set_top_p(self, new_top_p):
        self._top_p = new_top_p


    def set_max_tokens(self, new_max_tokens):
        self._max_tokens = new_max_tokens


    def set_stream(self, new_stream):
        self._stream = new_stream


    def set_llm_request_queue(self):
        self._llm_request_queue = LLMRequestQueue(self._queue_op_num, self._model, self._temperature, self._top_p, self._max_tokens, self._stream)


    def set_llm_communicator(self, request):
        self._llm_communicator = LLMCommunicator(self._url, self._model, request)


    def set_llm_message_handler(self, response):
        self._llm_message_handler = LLMMessageHandler(response)



    def run(self):
        pass


    def test_run(self, log_data, template, from_module, to_module):
        self.set_llm_request_queue()
        self._llm_request_queue.append_queue(log_data, template, from_module, to_module)
        batch = self._llm_request_queue.get_next_batch()
        for job in batch:
            self.set_llm_communicator(job)
            self.set_llm_message_handler(self._llm_communicator.run())
            self._llm_message_handler.handle_message()
