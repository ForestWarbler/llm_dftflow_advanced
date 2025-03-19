from payload import *
from llm_request import *
from llm_request_queue import *
from llm_response import *
from llm_communicator import *
from llm_message_handler import *

class LLMModule:
    def __init__(self, queue_op_num = 5, url = None, model = None):
        self._queue_op_num = queue_op_num
        self._url = url
        self._model = model
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


    def run(self):
        while self.check_all():
            pass

