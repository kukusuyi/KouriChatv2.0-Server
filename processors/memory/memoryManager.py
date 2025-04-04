import multiprocessing
from multiprocessing import Queue, Process
from typing import Dict, Any
import time
import logging
from dataclasses import dataclass, field
import json
import sys

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if sys.platform == 'win32': # 根据操作系统选择
    ctx = multiprocessing.get_context('spawn')
else:  # Linux/Unix
    ctx = multiprocessing.get_context('fork')  

@dataclass
class Message:
    """消息数据类"""
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)  # 使用 field
    
    def __reduce__(self):
        # 备注: 这里的 __reduce__ 方法是为了支持pickle序列化 ,且必须进行序列化
        """支持pickle序列化"""
        return (Message, (self.content, self.metadata))

# 将工作函数移到类外部
def search_worker_fn(input_queue: Queue, output_queue: Queue):
    """搜索工作进程函数"""
    while True:
        try:
            message = input_queue.get()
            if message is None:  # 停止信号
                break

            logger.info(f"Search worker processing message: {message.content}")
            time.sleep(1)  # 模拟耗时操作
            search_result = f"Search results for: {message.content}"
            output_queue.put(search_result)

        except Exception as e:
            logger.error(f"Search worker error: {e}")

def write_worker_fn(input_queue: Queue):
    """写入工作进程函数"""
    while True:
        try:
            message = input_queue.get()
            if message is None:  # 停止信号
                break

            logger.info(f"Write worker processing message: {message.content}")
            time.sleep(2)  # 模拟耗时操作
            logger.info(f"Message written to vector DB: {message.content}")

        except Exception as e:
            logger.error(f"Write worker error: {e}")

class EventBus:
    """事件总线核心类"""
    def __init__(self):
        self.search_queue = Queue()
        self.write_queue = Queue()
        self.result_queue = Queue()

        # 使用模块级函数而不是类方法
        self.search_worker = Process(
            target=search_worker_fn,
            args=(self.search_queue, self.result_queue)
        )
        self.write_worker = Process(
            target=write_worker_fn,
            args=(self.write_queue,)
        )

        self.search_worker.start()
        self.write_worker.start()

    def process_message(self, message: Message) -> str:
        """处理消息入口"""
        # 发送到搜索队列
        self.search_queue.put(message)
        # 发送到写入队列
        self.write_queue.put(message)

        # 等待并返回搜索结果
        search_result = self.result_queue.get()
        return search_result

    def shutdown(self):
        """关闭"""
        self.search_queue.put(None)
        self.write_queue.put(None)
        self.search_worker.join()
        self.write_worker.join()


class memoryProcessor:
    """Memory 处理器"""

    def __init__(self):
        self.event_bus = EventBus()

    def process_client_message(self, message_content: str) -> str:
        """处理客户端消息"""
        message = Message(content=message_content, metadata={"timestamp": time.time()})

        # 通过事件总线处理消息
        search_result = self.event_bus.process_message(message)

        return search_result

    def close(self):
        """关闭资源"""
        self.event_bus.shutdown()

    # 示例用法


if __name__ == "__main__":
    # 注意: Windows下使用 multiprocessing 必须保护主模块
    def main():
        rag_processor = memoryProcessor()

        while True:
            user_input = input("Enter a message (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                rag_processor.close()
                break
            else:
                result = rag_processor.process_client_message(user_input)
                print(f"Search result: {result}")

    # 确保所有多进程代码都在这个保护块内执行
    main()