from sqlalchemy.orm import joinedload
from workspace.fucheng.ai_agents.tests.db import Node, NodeRelationship, Session

from llm import auto_comment

class TreeFactory:
    def __init__(self, session):
        self.session = session

    def get_node_by_id(self, node_id):
        """通过ID获取单个节点"""
        return self.session.query(Node).filter(Node.node_id == node_id).first()

    def get_tree(self, root_id):
        """读取以某个节点为根的整棵树"""
        return self.session.query(Node).options(joinedload(Node.children)).filter(Node.node_id == root_id).first()

    def get_children(self, parent_id):
        """查询某个节点的所有子节点"""
        parent = self.get_node_by_id(parent_id)
        return parent.children if parent else []

    def get_parent(self, child_id):
        """查询某个节点的父节点"""
        relationship = self.session.query(NodeRelationship).filter(NodeRelationship.child_id == child_id).first()
        return self.get_node_by_id(relationship.parent_id) if relationship else None

    def get_siblings(self, node_id):
        """查询某个节点的所有兄弟节点（包括自己）"""
        parent = self.get_parent(node_id)
        return self.get_children(parent.node_id) if parent else []

    def add_node(self, name, user_id, parent_id=None, **kwargs):
        """增加一个节点"""
        new_node = Node(name=name, user_id=user_id, **kwargs)
        self.session.add(new_node)
        self.session.commit()
        if parent_id:
            relationship = NodeRelationship(parent_id=parent_id, child_id=new_node.node_id)
            self.session.add(relationship)
            self.session.commit()
        return new_node

    def update_node(self, node_id, **kwargs):
        """修改节点属性"""
        node = self.get_node_by_id(node_id)
        if node:
            for key, value in kwargs.items():
                if hasattr(node, key):
                    setattr(node, key, value)
            self.session.commit()

    def delete_node(self, node_id):
        """删除一个节点及其所有子节点"""
        node = self.get_node_by_id(node_id)
        if node:
            # 删除所有子节点
            for child in self.get_children(node_id):
                self.delete_node(child.node_id)
            # 删除节点本身
            self.session.delete(node)
            self.session.commit()

# 使用示例
# session = Session()  # 假设已经创建了SQLAlchemy session
# tree_factory = TreeFactory(session)
# root_node = tree_factory.add_node(name="Root Node", user_id=uuid.uuid4())
# child_node = tree_factory.add_node(name="Child Node", user_id=uuid.uuid4(), parent_id=root_node.node_id)

import os
import uuid

def walk_path_and_create_nodes(path, user_id, parent_id=None, session=None):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            # 这里假设每个文件都是一个Node
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as file_obj:
                file_content = file_obj.read()
                description = auto_comment(file_content)

            node = Node(
                name=file_name,
                node_type='file',  # 或者根据你的需要来设置
                description=description,
                data={'path': file_path, 'file_content': file_content},  # 存储文件路径或其他相关数据
                user_id=user_id,
                permission='public'  # 根据需要设置权限
            )
            session.add(node)
            session.commit()  # 提交每个节点以获取node_id

            if parent_id:
                # 如果这个节点有父节点，我们创建一个NodeRelationship
                relationship = NodeRelationship(parent_id=parent_id, child_id=node.node_id)
                session.add(relationship)
                session.commit()

        for dir_name in dirs:
            # 对于每个目录，我们也创建一个Node，并递归地处理它的内容
            dir_path = os.path.join(root, dir_name)
            dir_node = Node(
                name=dir_name,
                node_type='directory',
                description='A directory in the system, contains {}'.format(', '.join(os.listdir(dir_path))),
                data={'path': dir_path},
                user_id=user_id,
                permission='public'
            )
            session.add(dir_node)
            session.commit()  # 提交以获取node_id

            # 递归地处理这个目录
            walk_path_and_create_nodes(dir_path, user_id, parent_id=dir_node.node_id, session=session)


from langchain_core.documents.base import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector

embeddings_model = OpenAIEmbeddings()

def create_doc(content: str, meta: dict):
    content_doc = Document(page_content=content, metadata=meta)
    return content_doc

session = Session()  # 创建会话
user_id = '598a7fd4-6bff-4f07-918a-f07e452ab050'  # 假设你已经有了一个用户ID
knowledge_id = '598a7fd4-6bff-4f07-918a-f07e452ab050'  # 假设你已经有了一个知识库ID
# path_to_walk = '/home/ubuntu/workspace/opensource/naive-ui/src'

# walk_path_and_create_nodes(path_to_walk, user_id, session=session)
all_nodes = session.query(Node).all()
# 创建索引
metadata = {'user_id': str(user_id)}


texts = [create_doc(f'{r.name} 是 {r.node_type}: {r.description}', {'user_id':metadata['user_id'], 'doc_id':str(r.node_id)}) for r in all_nodes]

# # 将文章的向量索引保存到数据库
db = PGVector.from_documents(
    embedding=embeddings_model,
    documents=texts,
    collection_name='Navie UI',
    connection_string=os.environ['SQLALCHEMY_DATABASE_URL'],
)


        

