import asyncio
import concurrent.futures
from functools import partial

import sys
import os
import logging
from multiprocessing import Process, Manager
from time import time

from network import NetworkManager
from config import SettingReader
from globals.global_variable import GlobalVariable
from registry.handler_registry import HandlerRegistry

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
configs = SettingReader().get_config()
modols = SettingReader().get_model()
logger = logging.getLogger(__name__)


def dialogue_task(to_message_send_queue, to_message_get_queue):
    """ 对话处理进程： 该进程用于处理所有与对话发送相关的cpu密集任务
    return: 无返回值
    """
    # print("cpu密集任务")
    while True:
        message = to_message_get_queue.get()
        if message is None:  # 停止信号
            break
        # test
        print(f"获取到消息{message}")
        print("cpu密集任务")


async def main():
    # 获取网络管理器实例
    network_manager = NetworkManager()
    # 初始化全局变量

    process_pool = concurrent.futures.ProcessPoolExecutor()
    manager = Manager()
    GlobalVariable.init_queues(manager)

    try:
        # 启动所有服务器
        """
            协程启用进程
                不用线程的原因： 受限于 python 设计 GIL(全局解释锁) 无法同时在两个线程中同时执行cpu密集任务, 因此使用 **双进程** 的方式实现在单一程序内双线处理
                通信方式 消息接受进程「http接收」 -> to_message_send_queue -> 消息发送进程
                        消息发送进程 -> to_message_get_queue -> 消息接受进程
        """
        await asyncio.gather(
            network_manager.start_servers(),
            asyncio.get_event_loop().run_in_executor(process_pool, dialogue_task, GlobalVariable.to_message_send_queue, GlobalVariable.to_message_get_queue)
        )
        
    except asyncio.CancelledError:
        print("Received Ctrl+C, exiting gracefully.")
        # 确保进程池关闭  
        process_pool.shutdown(wait=True, cancel_futures=True)
        # 关闭事件循环
        asyncio.get_running_loop().stop()
    except Exception as e:
        print(f"程序异常终止: {str(e)}")
        await network_manager.shutdown()
    finally:
        if hasattr(network_manager, '_flask_task') and not network_manager._flask_task.done():
            await network_manager.shutdown()
        process_pool.shutdown(wait=True, cancel_futures=True) 
            

if __name__ == '__main__':    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序正在退出...")
    except asyncio.CancelledError:
        print("\n异步任务已取消")
    except Exception as e:
        print(f"\n程序异常退出: {str(e)}")
    finally:
        print("程序已退出")
        os._exit(0)
