from llm_request import LLMRequest
from llm_request_queue import LLMQueue


class LLMMessageHandler:
    def __init__(self):
        self.module_queues = {}


    def register_module_queue(self, module_name: str, queue: LLMQueue):
        self.module_queues[module_name] = queue


    def handle_message(self, request: LLMRequest, response):
        module_name = request.to_module
        if module_name in self.module_queues:
            self.module_queues[module_name].enqueue((request, response))
            print(f"Message for module '{module_name}' handled and enqueued.")
        else:
            print(f"Warning: No queue registered for module '{module_name}'. Message not handled.")
