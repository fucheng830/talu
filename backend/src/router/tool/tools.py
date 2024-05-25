
def init_request_tool(config):
    """
    pass
    """
    pass



navie_ui_str = """
# 引入tool
from langchain.tools import tool

from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores.pgvector import DistanceStrategy

from sqlalchemy import create_engine, Column, String, ForeignKey, JSON, Integer, DateTime, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'common'}

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    union_id = Column(String(255))
    openid = Column(String(255))
    name = Column(String(255))
    avatar = Column(String(255))
    subscribe_scene = Column(String(255))
    password = Column(String(255), nullable=False)
    phone_num = Column(String(20), unique=True)
    session_key = Column(String(255))
    vip_end_time = Column(DateTime)
    status = Column(Integer, default=1)
    register_time = Column(DateTime, default=func.now())
    user_info = Column(JSON)
    email = Column(String(100), unique=True)
    referee = Column(UUID(as_uuid=True))
    ip = Column(String(45))



class Node(Base):
    __tablename__ = 'nodes'
    __table_args__ = {'schema': 'data_store'}
    
    node_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    node_type = Column(String(255))
    description = Column(Text)
    data = Column(JSON)
    user_id = Column(UUID(as_uuid=True), ForeignKey('common.users.user_id'), nullable=False)
    permission = Column(String, default='public')
    
    children = relationship(
        "NodeRelationship",
        back_populates="parent",
        foreign_keys="[NodeRelationship.parent_id]",  # 明确指定使用哪个列作为外键
    )
    
    def __init__(self, name, node_type=None, description=None, data=None, user_id=None, permission='public'):
        self.name = name
        self.node_type = node_type
        self.description = description
        self.data = data
        self.user_id = user_id
        self.permission = permission

class NodeRelationship(Base):
    __tablename__ = 'node_relationships'
    __table_args__ = {'schema': 'data_store'}
    
    parent_id = Column(UUID(as_uuid=True), ForeignKey('data_store.nodes.node_id'), primary_key=True)
    child_id = Column(UUID(as_uuid=True), ForeignKey('data_store.nodes.node_id'), primary_key=True)
    
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

# 配置数据库连接（示例）
engine = create_engine('postgresql://postgres:Fucheng830@192.168.2.152:5433/postgres')
Session = sessionmaker(bind=engine)

embeddings_model = OpenAIEmbeddings()

store = PGVector(
    connection_string='postgresql://postgres:Fucheng830@192.168.2.152:5433/postgres', 
    embedding_function=embeddings_model, 
    collection_name='Navie UI',
    distance_strategy=DistanceStrategy.COSINE
)

retriever = store.as_retriever(search_kwargs={'k': 5})

# 定义检索工具
def retriever_tool(query: str) -> str:
    contents = []
    doc_ids = []
    for r in retriever.get_relevant_documents(query):
        doc_ids.append(str(r.metadata['doc_id']))
    
    with Session() as session:
        all_nodes = session.query(Node).filter(Node.node_id.in_(doc_ids)).all()
        for node in all_nodes:
            if node.node_type=='file':
                file_content = node.data['file_content']
                contents.append(file_content)
                
    return '\n\n'.join(contents)
    

tool_main=retriever_tool
"""


