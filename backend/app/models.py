from sqlalchemy import create_engine, Column, String, Integer, \
    ForeignKey, Float, Boolean, DateTime, Text, ARRAY, JSON, UniqueConstraint, CheckConstraint, \
        LargeBinary, Numeric, Date, \
    TIMESTAMP, BigInteger

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import BYTEA
from pgvector.sqlalchemy import Vector
import sqlalchemy
from datetime import datetime
from pgvector.sqlalchemy import Vector


Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    union_id = Column(String(255))
    openid = Column(String(255))
    name = Column(String(255))
    avatar = Column(String(255), default='avatar.jpg')
    subscribe_scene = Column(String(255))
    password = Column(String(255))
    phone_num = Column(String(20), unique=True)
    session_key = Column(String(255))
    vip_end_time = Column(DateTime)
    status = Column(Integer, default=1)
    register_time = Column(DateTime, default=func.now())
    user_info = Column(JSON, default={"usable_token": 20})
    email = Column(String(100), unique=True)
    referee = Column(UUID(as_uuid=True))
    ip = Column(String(45))

    files = relationship('File', back_populates='user')


class UserThirdPartyAccount(Base):
    __tablename__ = 'user_third_party_accounts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    third_party_name = Column(String(100), nullable=False)
    third_party_user_id = Column(String(255), nullable=False)
    additional_info = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

# conversation
class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    message_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    parent_message_id = Column(UUID(as_uuid=True), nullable=True)
    content = Column(String, nullable=False)
    embedding = Column(String, nullable=True)  # Assuming `pgvector` extension, use appropriate type
    role = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    conversation = relationship("Conversation", back_populates="messages")


# RAG
class Node(Base):
    __tablename__ = 'nodes'
    
    node_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    node_type = Column(String(255))
    description = Column(Text)
    data = Column(JSON)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    permission = Column(String, default='public')
    content = Column(Text)
    knowledge_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    children = relationship(
        "NodeRelationship",
        back_populates="parent",
        foreign_keys="[NodeRelationship.parent_id]",
    )
    
    def __init__(self, name, node_type=None, description=None, data=None, user_id=None, permission='public', content=None, knowledge_id=None):
        self.name = name
        self.node_type = node_type
        self.description = description
        self.data = data
        self.user_id = user_id
        self.permission = permission
        self.content = content
        self.knowledge_id = knowledge_id


class NodeRelationship(Base):
    __tablename__ = 'node_relationships'
    
    parent_id = Column(UUID(as_uuid=True), ForeignKey('nodes.node_id'), primary_key=True)
    child_id = Column(UUID(as_uuid=True), ForeignKey('nodes.node_id'), primary_key=True)
    
    parent = relationship(
        "Node", 
        foreign_keys=[parent_id], 
        back_populates="children",
        primaryjoin="NodeRelationship.parent_id==Node.node_id"  # 确保正确设置了 join 条件
    )
    child = relationship(
        "Node", 
        foreign_keys=[child_id],
        primaryjoin="NodeRelationship.child_id==Node.node_id"  # 确保正确设置了 join 条件
    )


class Knowledge(Base):
    __tablename__ = 'langchain_pg_collection'

    name = Column(String)
    cmetadata = Column(JSON)
    uuid = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID)

    embeddings = relationship(
            "EmbeddingStore",
            back_populates="collection",
            passive_deletes=True,
        )


class EmbeddingStore(Base):
    """Embedding store."""

    __tablename__ = "langchain_pg_embedding"

    collection_id = sqlalchemy.Column(
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey(
            f"{Knowledge.__tablename__}.uuid",
            ondelete="CASCADE",
        ),
    )
    collection = relationship(Knowledge, back_populates="embeddings")

    embedding: Vector = sqlalchemy.Column(Vector())
    document = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cmetadata = sqlalchemy.Column(JSONB, nullable=True)

    # custom_id : any user defined id
    custom_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    uuid = sqlalchemy.Column(
        UUID(as_uuid=True), primary_key=True
    )


class File(Base):
    __tablename__ = 'files'

    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(255), nullable=False)
    cloud_storage_identifier = Column(String(255))
    upload_time = Column(DateTime, default=func.now())
    file_size = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    group_id = Column(UUID(as_uuid=True))
    
    user = relationship('User', back_populates='files')


class FileContent(Base):
    __tablename__ = 'file_content'

    id = Column(String(64), primary_key=True)
    file_data = Column(LargeBinary)


class Document(Base):
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True)
    doc_name = Column(String(255), nullable=False)
    doc_content = Column(String(255), nullable=False)
    upload_time = Column(DateTime, default=func.current_timestamp())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    group_id = Column(UUID(as_uuid=True))
    knowledge_id = Column(UUID(as_uuid=True), ForeignKey('langchain_pg_collection.uuid'))
    # Define the relationship to the User class, assuming it is defined with 'common.users' as the table name.
    user = relationship('User', backref='documents')


class Image(Base):
    __tablename__ = 'images'

    id = Column(String(255), primary_key=True)
    image_data = Column(BYTEA, nullable=False)
    format = Column(String(20), nullable=False)
    source_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


# Agent
class AgentCategory(Base):
    __tablename__ = 'agent_category'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)


class Agent(Base):
    __tablename__ = 'agent'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    system_prompt = Column(String)
    opening_question = Column(JSON)
    knowledge = Column(JSON)
    tools = Column(JSON)
    voice = Column(String)
    avatar = Column(String)
    suggestion = Column(JSON)
    user_id = Column(String)
    permission = Column(String, default='temp')
    category = Column(String)
    llm = Column(JSON, default={"model": "gpt-3.5-turbo", "temperature": 0.8, "streaming": True})
    gid = Column(String)
    opening_text = Column(String)


class ToolConfig(Base):
    __tablename__ = 'tool'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    func = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    code = Column(Text, nullable=False)
    permission = Column(String, nullable=False)
    avatar = Column(String, nullable=False)


class LLMConfig(Base):
    __tablename__ = 'llm_config'  # 表名

    id = Column(Integer, primary_key=True, autoincrement=True)  # 配置ID，自动递增的主键
    model_provider = Column(String(50), nullable=False)  # 模型提供者名称
    model_name = Column(String(100), nullable=False)  # 模型名称
    module_name = Column(String(100), nullable=False)  # 模块名称
    icon_url = Column(String(255))  # 图标URL
    supports_tool_calling = Column(Boolean, nullable=False)  # 是否支持工具调用
    supports_structured_output = Column(Boolean, nullable=False)  # 是否支持结构化输出
    supports_json_mode = Column(Boolean, nullable=False)  # 是否支持JSON模式
    is_local = Column(Boolean, nullable=False)  # 是否为本地模型
    supports_multimodal = Column(Boolean, nullable=False)  # 是否支持多模态
    library_package = Column(String(100), nullable=False)  # 库包名称






# Define the Plan, Discount, UserSubscription, Rebate, Order, and Withdrawal classes here

class Referral(Base):
    __tablename__ = 'referral'

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    referee_id = Column(UUID(as_uuid=True), nullable=False)
    rebate = Column(Float, default=0.0)


class Plan(Base):
    __tablename__ = 'plans'  # 表名应该与数据库中的名称匹配，注意大小写和引号

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    base_price = Column(Numeric, nullable=False)
    chat_limit = Column(Integer, nullable=False)
    store_limit = Column(Integer, nullable=False)
    expire_days = Column(Integer, default=30, nullable=False)
    daily_chat_count = Column(Integer, default=100, nullable=False)
    creatable_role_count = Column(Integer, default=5, nullable=False)
    creatable_knowledge_count = Column(Integer, default=5, nullable=False)

    def __repr__(self):
        return f"<Plan(name={self.name}, base_price={self.base_price}, chat_limit={self.chat_limit})>"


class Discount(Base):
    __tablename__ = 'discounts'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    period = Column(Integer, nullable=False)
    discount_percent = Column(Numeric, nullable=False)



class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    period = Column(Integer, nullable=False)
    effective_price = Column(Numeric, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)



class Rebate(Base):
    __tablename__ = 'rebates'

    id = Column(Integer, primary_key=True)
    referrer_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    beneficiary_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    order_id = Column(BigInteger, ForeignKey('orders.order_id'), nullable=False)
    rebate_amount = Column(Numeric, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(Date, default=datetime.utcnow, nullable=False)
    paid_at = Column(Date)

    # Relationships
    referrer = relationship("User", foreign_keys=[referrer_id])
    beneficiary = relationship("User", foreign_keys=[beneficiary_id])
    order = relationship("Order")



class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(BigInteger, primary_key=True)  # 主键
    user_id = Column(String(255), nullable=False)
    plan_id = Column(Integer, nullable=False)
    trade_type = Column(String(50), nullable=False)
    price = Column(Numeric, nullable=False)
    status = Column(String(50), default='unpaid', nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    pay_info = Column(JSONB, nullable=False)
    vip_end_time = Column(TIMESTAMP, nullable=False)



class Withdrawal(Base):
    __tablename__ = 'withdrawals'

    withdrawal_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), nullable=False)
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    response = Column(JSONB)  # Optional: stores JSON data for responses or errors


