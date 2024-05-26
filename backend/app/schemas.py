from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserSchema(BaseModel):
    user_id: UUID4
    union_id: Optional[str]
    openid: Optional[str]
    name: str
    avatar: Optional[str]
    subscribe_scene: Optional[str]
    password: str  # Consider handling passwords more securely
    phone_num: str
    session_key: Optional[str]
    vip_end_time: Optional[datetime]
    status: int
    register_time: datetime
    user_info: Optional[dict]
    email: str
    referee: Optional[UUID4]
    ip: Optional[str]

    class Config:
        orm_mode = True

class ThirdPartyAccountBinding(BaseModel):
    user_id: UUID4 = Field(description="The ID of the user to bind the third-party account to.")
    third_party_name: str = Field(description="The name of the third-party service (e.g., 'google', 'facebook').")
    third_party_user_id: str = Field(description="The user's ID according to the third-party service.")
    additional_info: Optional[dict] = Field(default={}, description="Any additional information related to the third-party account.")


class Link(BaseModel):
    url: str

class ContentParams(BaseModel):
    url: str

class SearchParams(BaseModel):
    text: str


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 10

class SuggestionConfig(BaseModel):
    is_enable: bool
    custom_prompt: Optional[str] = None


class AgentBase(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    opening_text: Optional[str] = None
    opening_question: list[str] = None
    system_prompt: Optional[str] = None
    knowledge: Optional[list] = []
    tools: Optional[list] = []
    voice: Optional[str] = None
    avatar: Optional[str] = None
    suggestion: Optional[SuggestionConfig] = None
    permission: Optional[str]
    category: Optional[str] = None
    gid: Optional[str] = None

    class Config:
        orm_mode = True

class AgentFilter(BaseModel):
    just_user: Optional[str]
    class Config:
        orm_mode = True


class AgentQuery(BaseModel):
    id: str


class KnowledgeSchema(BaseModel):
    name: str
    type: str

    class Config:
        orm_mode = True

class DocumentCreate(BaseModel):
    doc_name: str
    doc_content: str
    group_id: Optional[UUID] = None
    knowledge_id: Optional[UUID] = None

    class Config:
        orm_mode = True


class SplitText(BaseModel):
    file_id: str
    class Config:
        orm_mode = True


class KnowledgeDeleteSchema(BaseModel):
    knowledge_id: str


class SplitHandler(BaseModel):
    documents: list
    handler_name: str
    params: dict


class ManulDocument(BaseModel):
    name: str
    knowledge_id: str
    
    
class ManualDocumentContent(BaseModel):
    node_id: str
    answer: str
    question: str
    knowledge_id: str


class uploadDatas(BaseModel):
    data: list[dict]
    knowledge_id: str

class knowledgeId(BaseModel):
    knowledge_id: str

class deleteParams(BaseModel):
    node_id: str

class segmentPreview(BaseModel):
    node_id: str
    
# Pydantic 模型，用于 POST 请求体
class ScannerCallbackBody(BaseModel):
    user_info: dict
    qr_scene: str


class ScanQrParams(BaseModel):
    scene_id: int
    referee: Optional[str] = None

class GetNodeDataParams(BaseModel):
    node_id: str

class AddUrlContentParams(BaseModel):
    url: str
    knowledge_id: str

class SearchNodeParams(BaseModel):
    query: str
    knowledge_id: str
    search_config: Optional[dict] = {}


class UserSubscriptionParams(BaseModel):
    plan_id: int = Field(..., description="ID of the plan being subscribed to")

    class Config:
        orm_mode = True

class PayParams(BaseModel):
    id: str
    plan_id: int # 订阅计划ID
    trade_type: str # 支付环境 pc, h5, wechat

class OrderRequest(BaseModel):
    order_id: int