"""
Global variables
全局变量
"""
from queue import Queue
from typing import Optional

from config import SettingReader
from registry import HandlerRegistry


# from multiprocessing import Manager


class GlobalVariable:
    _var = {} # 通用全局变量，需要使用自行添加
    handlerRegistry = None # 处理器注册器
    to_message_get_queue:Queue = None  # 进程通信队列 消息接收进程
    to_message_send_queue:Queue = None  # 进程通信队列 消息发送进程
    rag_url = None
    config = None

    #
    def __init__(self) -> None:
        pass

    @classmethod
    def init_queues(cls,manager):
        cls.to_message_get_queue = manager.Queue(-1) # 进程通信队列 消息接收进程
        cls.to_message_send_queue = manager.Queue(-1) # 进程通信队列 消息发送进程
    @classmethod
    def init_handler_registry(cls):
        cls.handlerRegistry = HandlerRegistry()
    @classmethod
    def init_config(cls):
        cls.config = SettingReader().get_config()
    @classmethod
    def set(cls, key, value):
        cls._var[key] = value
    
    @classmethod
    def get(cls, key):
        return cls._var.get(key)
    
    @classmethod
    def delete(cls, key):
        del cls._var[key]
    

    @classmethod
    def clear(cls):
        cls._var.clear()