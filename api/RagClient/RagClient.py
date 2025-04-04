from api.HttpUtil import Http
from api.RagClient.models import ChatList, ChatMessage, CreateChat


class RagClient(object):
    def __init__(self, base_url):
        # rag 地址
        self.base_url = base_url
        self.http = Http(base_url)

    """发送chat消息"""
    def post_chat(self, chatMessage: ChatMessage):
        try:
            return self.http.post('/api/chat/conversation_chat',json=chatMessage)
        except Exception as e:
            print(e)
            return None

    """获取chat列表"""
    def get_chat_list(self, chatList: ChatList | None = None):
        if chatList is None:
            chatList = ChatList()
        try:
            return self.http.get('/api/conversation/conversations', params=chatList)
        except Exception as e:
            print(e)
            return None
    
    """创建chat"""
    def create_chat(self, createChat: CreateChat):
        try:
            return self.http.post('/api/conversation',json=createChat)
        except Exception as e:
            print(e)
            return None