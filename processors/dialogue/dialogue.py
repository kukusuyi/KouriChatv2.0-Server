"""对话处理器：
    负责处理对话逻辑,提取有效信息，发送有效信息
    对话处理流程：
        message_routes(获取信息) -> to_message_get_queue -> DialogueProcessor -> 提取信息, 处理信息 -> 发送信息
    对话处理器收到信息后的处理流程:
        dialogue_processor -> processMessage(判断消息类型）-> _type_process_message -> 建立 rag_client 映射
        -> 获取 rag 内容 -> 发送 rag 内容
"""
import json
from itertools import count
from typing import Union
import paho.mqtt.client as mqtt

from api.RagClient import RagClient
from api.RagClient.models import ChatMessage, CreateChat
from config import SettingReader
from globals.global_variable import GlobalVariable
from models.message import TextMessage


class dialogueProcessor:
    """ TODO: 一个用户实例一个dialogueProcessor 并使用映射表进行管理"""
    context_rag_mapper = {} # id 映射表

    def __init__(self):
        print('init dialogueProcessor')

    def processMessage(self,message:Union[TextMessage]): # 联合消息类型，消息类型来自于 models 下，请仔细甄别
        if message.message_type == "text":
            return self._text_process_message(message)

    def _text_process_message(self,message:TextMessage):
        """text 消息处理"""
        if message.sender_id not in self.context_rag_mapper: # 如果没有映射关系，建立映射关系,建立映射关系后，会自动发送消息
            # 获取该用户配置的 rag_baseurl TODO(为后期多用户预留)
            RagClient.update_count() # TODO: 这里需要考虑一个极端情况，在请求rag当前对话列表时，另一个用户同时请求该列表，rag方面需要做出锁限制，或是create对话列表时候可以传入指定参数
            self.context_rag_mapper[message.sender_id] = RagClient.count + 1
            create_chat = CreateChat(f"用户{RagClient.count + 1}")
            RagClient.create_chat(create_chat)

        # 构造 ChatMessage
        chat_message = ChatMessage(self.context_rag_mapper[message.sender_id],message.content)
        res = RagClient.post_chat(chat_message)
        json_string = json.dumps(res.json(), ensure_ascii=False)
        client = mqtt.Client()
        try:
            client.connect(GlobalVariable.config['categories']['mqtt_setting']['ip'], GlobalVariable.config['categories']['mqtt_setting']['port'], GlobalVariable.config['categories']['mqtt_setting']['keepalive'])
            client.publish(str(message.sender_id), json_string,qos=1)
        except Exception as e:
            print(f"MQTT Error: {e}")



if __name__ == '__main__':
    GlobalVariable.init_config()
    text_message = TextMessage(sender_id=123,sender="susu",chat_type="qq",character=1,message_type="text",message_send_time="2024-04-21 12:00:00",content="你好")
    dialogue_processor = dialogueProcessor()
    dialogue_processor.processMessage(text_message)

