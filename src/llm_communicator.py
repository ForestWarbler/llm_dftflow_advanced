from src.llm_request import LLMRequest
from src.llm_request_queue import LLMRequestQueue
from src.llm_response import LLMResponse
import re
import requests
import json

class LLMCommunicator:
    def __init__(self, url, model, request):
        self._url = url
        self._model = model
        self._request = request

    def send_to_llm(self):
        # 从 request 对象中获取 payload
        to_module = self._request.get_to_module()
        payload = self._request.get_payload()
        # 构造请求数据，包含模型和 payload
        headers = {
            "Content-Type": "application/json"
        }
        try:
            # 发送 POST 请求给 LLM 服务
            response = requests.post(self._url, json=payload, headers=headers)
            response.raise_for_status()  # 如果响应状态码不是 200，将抛出异常
            # 返回解析后的 JSON 数据作为回复
            response_class = LLMResponse(to_module, response.json())

            return response_class
        except requests.exceptions.RequestException as e:
            print("请求 LLM 时出错:", e)
            return None

    def run(self):
        # 通过 send_to_llm 方法发送请求并获取回复
        reply = self.send_to_llm()
        return reply