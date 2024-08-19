
from typing import List, Dict
from sqlalchemy import desc
from sqlalchemy.orm import Session
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import sqlalchemy
import uuid


from ...models import *
from ...config import lite_model_name


embeddings_model = OpenAIEmbeddings()


def summary_chain(content):
    llm = ChatOpenAI(temperature=0, model_name=lite_model_name) 
    prompt = f"""
请总结以下内容：
{content}
    """
    result = llm.invoke(prompt)
    return result


# 最近的n条消息策略
def get_last_messages(conversation_id: uuid.UUID, max_context_len: int, user_id:uuid.UUID, db: Session):
    messages = db.query(Message).filter_by(conversation_id=conversation_id, user_id=user_id).order_by(desc(Message.created_at)).limit(max_context_len).all()
    return messages[::-1]  # Reverse to maintain chronological order


# 进行汇总
def summarize_messages(conversation_id: uuid.UUID, max_context_len: int, user_id:uuid.UUID, db: Session):
    # 简单的消息汇总实现，实际中可以用更复杂的算法
    conversation = db.query(Conversation).filter_by(conversation_id=conversation_id, user_id=user_id).first()
    messages = get_last_messages(conversation_id, max_context_len, user_id, db)
    context = " ".join([msg.content for msg in messages])
    summary = conversation.summary
    if conversation.summary: 
        summary += context
    else:
        summary = context
        
    summary = summary_chain(summary)
    conversation.summary = summary
    db.commit()
    return [HumanMessage(content=summary)]


# 基于向量的搜索
def rag_search(conversation_id: uuid.UUID, max_context_len: int, user_id:uuid.UUID, prompt_embedding: List, db: Session):
    # 简单的向量搜索实现，实际中应该使用向量数据库或嵌入技术
    # 这里仅示例返回前 max_context_len 个消息
    distance_strategy = Message.embedding.cosine_distance
    messages = (db.query(Message,
               distance_strategy(prompt_embedding).label("distance"),
                         ).filter_by(conversation_id=conversation_id, user_id=user_id)
    .order_by(sqlalchemy.asc("distance"))
    .limit(max_context_len)
    .all())
    return [result[0] for result in messages]
    

def process_context_compression(strategy: str, conversation_id: uuid.UUID, max_context_len: int, prompt_embedding:List, user_id:uuid.UUID, db: Session) -> List[Dict]:
    """上下文压缩"""
    if strategy == 'keep_last':
        return get_last_messages(conversation_id, max_context_len, user_id, db)
    elif strategy == 'summary':
        return summarize_messages(conversation_id, max_context_len, user_id, db)
    elif strategy == 'rag':
        return rag_search(conversation_id, max_context_len, user_id, prompt_embedding, db)
    else:
        raise ValueError("Invalid context_compress_strage value")


def load_context_message(strategy, conversation_id, max_context_len, prompt_embedding, user_id, db):
    """加载上下文消息"""
    messages_len = db.query(Message).filter_by(conversation_id=conversation_id,user_id=user_id).count()
    if messages_len > max_context_len:
        messages = process_context_compression(strategy, conversation_id, max_context_len, prompt_embedding, user_id, db)
    else:
        messages = db.query(Message).filter_by(conversation_id=conversation_id,user_id=user_id).all()
    return messages




  
