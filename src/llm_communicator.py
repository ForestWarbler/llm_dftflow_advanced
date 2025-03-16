import time
import logging
import requests

from llm_queue import LLMRequestQueue  # 使用提供的 LLMRequestQueue 管理任务队列
import payload


class LLMCommunicator:
    def __init__(self, url, model, batch_size=5, poll_interval=3):
        """
        初始化 LLMCommunicator

        参数:
            url: LLM 服务的访问 URL
            model: 要使用的模型名称
            batch_size: 每次批处理任务的数量（默认为5），同时用于设置队列的 op_num
            poll_interval: 轮询队列的时间间隔（单位：秒，默认为3秒）
        """
        self.url = url
        self.model = model
        self.poll_interval = poll_interval
        # 使用 LLMRequestQueue 管理任务队列，将 op_num 设置为 batch_size
        self.queue = LLMRequestQueue(op_num=batch_size)

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def get_batch(self):
        """
        从队列中获取一批任务

        返回:
            tasks: 任务列表（可能为空列表）
        """
        tasks = self.queue.get_next_batch()
        return tasks

    def send_batch(self, tasks):
        """
        发送批处理任务

        参数:
            tasks: 任务列表（LLMRequest 对象列表）

        返回:
            response: LLM 返回的信息（解析为字典或列表）或 None
        """
        if not tasks:
            logging.info("当前批次任务为空，无需发送。")
            return None

        # 构造请求负载，假设 payload.create_payload 接受 LLMRequest 对象列表并返回字典
        request_payload = payload.create_payload(tasks)
        # 将 model 信息添加到请求负载中
        request_payload['model'] = self.model
        logging.info("构造请求负载：%s", request_payload)

        try:
            # 使用 requests.post() 发送 HTTP 请求到 LLM 服务
            response = requests.post(self.url, json=request_payload)
            if response.status_code == 200:
                logging.info("收到 LLM 响应。")
                return response.json()
            else:
                logging.error("请求失败，状态码: %s, 响应: %s",
                              response.status_code, response.text)
                return None
        except Exception as e:
            logging.error("发送请求过程中出现异常: %s", e)
            return None

    def process_response(self, tasks, response):
        """
        处理 LLM 返回的响应信息

        参数:
            tasks: 本次发送的任务列表，对应此次请求
            response: LLM 返回的数据（解析为字典或列表）
        """
        if response is None:
            logging.warning("无有效响应可处理。")
            return

        # 这里假设响应中的结果顺序与任务顺序一致，或响应中有任务标识字段
        # 根据实际响应格式进行调整
        for i, task in enumerate(tasks):
            # 例如，假设 response 为列表，顺序对应 tasks
            result = response[i] if isinstance(response, list) and i < len(response) else None
            logging.info("任务 [%s] 的结果: %s", task, result)
            # 注意：由于任务已通过 get_next_batch 弹出，无需再进行标记完成操作

    def run(self):
        """
        启动轮询，不断从队列中获取任务、发送请求并处理响应
        """
        logging.info("LLM Communicator 启动...")
        while True:
            tasks = self.get_batch()
            if tasks:
                logging.info("发送批处理任务，任务数: %d", len(tasks))
                response = self.send_batch(tasks)
                self.process_response(tasks, response)
            else:
                logging.info("队列中无任务，等待下一次轮询...")
            time.sleep(self.poll_interval)


if __name__ == '__main__':
    # 示例：设置 LLM 服务 URL 和模型名称
    communicator = LLMCommunicator(url="http://example.com/llm",
                                   model="gpt-3.5-turbo",
                                   batch_size=5,
                                   poll_interval=3)
    communicator.run()
