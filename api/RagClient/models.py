from dataclasses import dataclass
from typing import List, Optional, Dict


# 获取对话回复

@dataclass
class ChatMessage(dict):
    conversation_id: int # 对话ID (必填)
    message: str # 用户消息
    use_memory: bool # 是否使用记忆功能
    use_knowledge: bool # 是否使用知识库
    knowledge_query: str # 知识库搜索查询，如果为None则使用message
    knowledge_limit: int # 知识库搜索结果数量限制
    use_web_search: bool # 是否使用网络搜索，默认为False，启用后AI将根据网络搜索结果辅助回答问题
    web_search_query: str # 网络搜索查询，如果为None则使用message
    web_search_limit: int # 网络搜索结果数量限制，默认为3
    conversation_files: List[str] # 关联到此对话的文件ID列表
    temperature: float # 温度参数，控制随机性，范围0-1.0，默认使用配置或对话设置
    max_tokens: int # 最大生成token数，默认使用配置中的值(4096)

    def __init__(self, conversation_id: int = 0, message: str = "", use_memory: bool = True, use_knowledge: bool = True,
                 knowledge_query: str = "", knowledge_limit: int = 0, use_web_search: bool = True,
                 web_search_query: str | None = None, web_search_limit: int = 3, conversation_files: List[str] = [],
                 temperature: float = 0.5, max_tokens: int = 1000):
        super().__init__()
        if not conversation_id:
            raise ValueError("conversation_id is required")
        if not message:
            raise ValueError("message is required")
        self.conversation_id = conversation_id
        self.message = message
        self.use_memory = use_memory
        self.use_knowledge = use_knowledge if knowledge_query is not None else message
        self.knowledge_query = knowledge_query
        self.knowledge_limit = knowledge_limit
        self.use_web_search = use_web_search
        self.web_search_query = web_search_query if web_search_query is not None else message
        self.web_search_limit = web_search_limit
        self.conversation_files = conversation_files or []
        self.temperature = temperature
        self.max_tokens = max_tokens


# 创建新对话

@dataclass
class CreateChat(dict):
    title: str  # 对话标题
    description: str | None= None  # 对话描述(可选)
    settings: Optional[Dict] = None  # 对话设置(可选) TODO: 完善对话设置的类型
    files: List[str] | None = None  # 关联的文件ID列表(可选)
    temperature: float = 0.7  # 温度参数，控制随机性，范围0-1.0，默认使用配置或对话设置
    max_tokens: int = 4096  # 最大生成token数，默认使用配置中的值(4096)

    def __post_init__(self):
        if self.files is None:
            self.files = []
        if self.settings is None:
            self.settings = {}


# 获取对话列表
@dataclass
class ChatList(dict):
    page: int = 1  # 页码
    page_size: int = 20  # 每页大小

    def __post_init__(self):
        if self.page < 1:
            self.page = 1