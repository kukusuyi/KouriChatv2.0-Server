import logging

from api.HttpUtil import Http
from api.RagClient.models import ChatList, ChatMessage, CreateChat
from globals.global_variable import GlobalVariable

logger = logging.Logger("RagClient")
class RagClient(object):
    _http = None
    count = 0
    """初始化"""
    def __init__(self, base_url):
        # rag 地址
        self.base_url = base_url
        self.http = Http(base_url)

    @classmethod
    def _init_http(cls):
        cls._http = Http(GlobalVariable.config['categories']['rag_setting']['url'])
        res = cls._get_chat_list()
        cls.count = res.json()['items'][0]['id']

    @classmethod
    def update_count(cls):
        res = cls._get_chat_list()
        cls.count = res.json()['items'][0]['id']

    """发送chat消息"""
    @classmethod
    def post_chat(cls, chatMessage: ChatMessage):
        if cls._http is None:
            cls._init_http()
        try:
            return cls._http.post('/api/chat/conversation_chat',json=chatMessage)
        except Exception as e:
            print(e)
            return None

    """获取chat列表"""
    @classmethod
    def _get_chat_list(cls, chatList: ChatList | None = None):
        if cls._http is None:
            cls._init_http()
        if chatList is None:
            chatList = ChatList()
        try:
            logger.info(cls._http)
            return cls._http.get('/api/conversation/conversations', params=chatList)
        except Exception as e:
            logger.error(e)
            return None
    
    """创建chat"""
    @classmethod
    def create_chat(cls, createChat: CreateChat):
        if cls._http is None:
            cls._init_http()
        try:
            return cls._http.post('/api/conversation',json=createChat)
        except Exception as e:
            print(e)
            return None