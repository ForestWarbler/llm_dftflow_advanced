from collections import deque
from src.payload import Payload
from src.llm_request import LLMRequest

class LLMRequestQueue:
    def __init__(self, op_num=5, model = None, temperature = 0, top_p = 1, max_tokens = 128000, stream = False):
        """
        初始化队列
        :param op_num: 每次按批操作时处理的请求数量
        """
        self._queue = deque()
        self._op_num = op_num
        self._model = model
        self._temperature = temperature
        self._top_p = top_p
        self._max_tokens = max_tokens
        self._stream = stream


    def set_op_num(self, op_num: int):
        """
        手动设置 op_num
        :param op_num: 每次按批操作时处理的请求数量
        """
        if op_num <= 0:
            raise ValueError("op_num 必须大于 0")
        self._op_num = op_num


    def get_op_num(self) -> int:
        """
        获取当前的 op_num
        :return: op_num
        """
        return self._op_num


    def add_requests_in_batch(self, requests):
        """
        批量添加 LLMRequest
        :param requests: 可迭代的 LLMRequest 列表或生成器
        """
        for req in requests:
            self._queue.append(req)


    def add_request(self, request):
        """
        添加单个 LLMRequest
        :param request: LLMRequest 实例
        """
        self._queue.append(request)


    def get_next_batch(self):
        """
        从队列中弹出下一批请求
        :return: 包含最多 op_num 个 LLMRequest 的列表
        """
        batch = []
        for _ in range(min(self._op_num, len(self._queue))):
            batch.append(self._queue.popleft())
        return batch


    def get_total_tasks(self) -> int:
        """
        获取队列中剩余任务数量
        :return: 队列的长度
        """
        return len(self._queue)


    def create_payload(self, log_data, template):
        payload = Payload()
        payload.set_model(self._model)
        payload.set_temperature(self._temperature)
        payload.set_top_p(self._top_p)
        payload.set_max_tokens(self._max_tokens)
        payload.set_stream(self._stream)
        # payload.set_messages(log_data, template)
        payload.setup_payload(log_data, template)
        return payload


    def create_request(self, payload, from_module, to_module):
        request = LLMRequest(payload, from_module, to_module)
        return request


    def append_queue(self, log_data, template, from_module, to_module):
        self.add_request(self.create_request(self.create_payload(log_data, template), from_module, to_module))

# =============== 使用示例 ===============

if __name__ == "__main__":
    # 假设已经有一个简单的 LLMRequest 示例类
    class LLMRequest:
        def __init__(self, prompt):
            self.prompt = prompt

        def __repr__(self):
            return f"LLMRequest({self.prompt})"

    queue = LLMRequestQueue(op_num=3)

    # 一次添加多个
    reqs = [LLMRequest(f"prompt_{i}") for i in range(5)]
    queue.add_requests_in_batch(reqs)

    print("当前队列任务总数：", queue.get_total_tasks())  # 输出 5

    # 获取一批请求
    batch1 = queue.get_next_batch()
    print("取出一批请求：", batch1)
    print("取出后剩余任务数：", queue.get_total_tasks())  # 输出 2

    # 动态修改 op_num
    queue.set_op_num(2)

    # 再添加一些请求
    queue.add_requests_in_batch([LLMRequest(f"prompt_{i}") for i in range(5, 8)])
    print("新添加后任务数：", queue.get_total_tasks())  # 2 + 3 = 5

    # 再取一批
    batch2 = queue.get_next_batch()
    print("取出一批请求：", batch2)
    print("取出后剩余任务数：", queue.get_total_tasks())