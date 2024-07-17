from langchain_core.documents.base import Document as LangchainDocument
from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy import text
import os
from langchain_core.documents.base import Document as LangchainDocument
from langchain_community.embeddings import OpenAIEmbeddings
from itertools import chain

from ....models import Node, EmbeddingStore
from ..pgvector import PGVector


def save_document(user_id, document, db):
    """
    保存或更新单个文档内容
    """
    if document.get("node_id"):
        print("node_id", document["node_id"])
        new_container = update_existing_document(document, db)
    else:
        new_container = create_new_document(user_id, document, db)
    texts = generate_texts(new_container, document, user_id)
    save_embeddings(texts, new_container.knowledge_id)
    return new_container


def update_existing_document(document, db):
    """
    更新现有文档内容并删除原有向量索引
    """
    new_container = db.query(Node).filter(Node.node_id == document["node_id"]).first()
    if not new_container:
        raise HTTPException(status_code=404, detail="Document not found")
    new_container.content = document["content"]
    db.query(EmbeddingStore).filter(
        text("cmetadata->>'doc_id' = :node_id")
    ).params(node_id=str(document["node_id"])).delete()
    db.commit()
    return new_container


def create_new_document(user_id, document, db):
    """
    创建新文档
    """
    new_container = Node(
        name=document["name"],
        node_type=document["type"],
        description=document.get("summary"),
        data={},
        knowledge_id=document["knowledge_id"], 
        content=document["content"],
        user_id=user_id,
    )
    db.add(new_container)
    db.commit()
    db.refresh(new_container)
    return new_container


def save_embeddings(documents, knowledge_id):
    """
    保存文档的向量嵌入
    """
    embeddings_model = OpenAIEmbeddings()
    PGVector.from_documents(
        connection_string=os.environ["SQLALCHEMY_DATABASE_URL"],
        collection_id=knowledge_id,
        embedding=embeddings_model,
        documents=documents,
    )


def generate_summary_text(new_container, user_id):
    """
    生成文档摘要文本对象
    """
    return [
        LangchainDocument(
            page_content=f"{new_container.name} 是 {new_container.node_type}: {new_container.description}",
            metadata={
                "user_id": user_id,
                "doc_id": str(new_container.node_id),
                "index_type": "summary",
            },
        )
    ]


def generate_content_texts(new_container, document, user_id):
    """
    生成文档内容文本对象
    """
    return [
        LangchainDocument(
            page_content=text_segment,
            metadata={
                "user_id": user_id,
                "doc_id": str(new_container.node_id),
                "index_type": "content",
                "index_id": i,
            },
        )
        for i, text_segment in enumerate(document["content_split"])
    ]


def generate_qa_texts(new_container, document, user_id):
    """
    生成文档问答文本对象
    """
    return [
        LangchainDocument(
            page_content=qa["question"],
            metadata={
                "user_id": user_id,
                "doc_id": str(new_container.node_id),
                "index_type": "qa",
                "answer": qa["answer"],
            },
        )
        for qa in document.get('qa', {}).get('qa_list', [])
    ]


def generate_texts(new_container, document, user_id):
    """
    生成文本对象列表用于向量嵌入
    """
    return list(chain(
        generate_summary_text(new_container, user_id),
        generate_content_texts(new_container, document, user_id),
        generate_qa_texts(new_container, document, user_id)
    ))
