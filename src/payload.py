class Payload:
    def __init__(self):
        self._model = None
        self._messages = None
        self._temperature = None
        self._top_p = None
        self._max_tokens = None
        self._stream = None
        self._payload = None


    def set_model(self, model):
        self._model = model


    def set_messages(self, log_data, template):
        self._messages = [
            {"role": "user",
             "content": f"Analyze the following logs and provide insights or errors if any:\n{log_data}"},
            {"role": "user", "content": "Based on the provided log lines, suggest possible errors or improvements."},
            {"role": "user", "content": f"Response Template:\n{template}"}
        ]


    def set_temperature(self, temperature):
        self._temperature = temperature


    def set_top_p(self, top_p):
        self._top_p = top_p


    def set_max_tokens(self, max_tokens):
        self._max_tokens = max_tokens


    def set_stream(self, stream):
        self._stream = stream


    def setup_payload(self):
        """
        根据传入的 log_data 和 template_content，及指定的模型和参数，
        构造最终的请求数据 payload。
        """
        # 如果需要在这里直接构造 messages，也可以不使用 set_messages()
        # 方法来存储 self._messages，而是直接写死如下三段消息
        self._payload = {
            "model": self._model,
            "messages": self._messages,
            "temperature": 0 if self._temperature is None else self._temperature,
            "top_p": 1 if self._top_p is None else self._top_p,
            "max_tokens": 128000 if self._max_tokens is None else self._max_tokens,
            "stream": False if self._stream is None else self._stream
        }
        return self._payload


    def get_payload(self):
        return self._payload