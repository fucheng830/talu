from fastapi import Request, APIRouter
from fastapi import Depends, HTTPException
import json


from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain.adapters.openai import convert_dict_to_message
from ..common.auth import get_current_user
import re
from ..sse_format import sse_json
from sse_starlette.sse import EventSourceResponse

# 对话路由接口
from langchain_community.adapters.openai import convert_dict_to_message
from ...models import *
from .memory import embeddings_model, load_context_message

from ...database import get_db
from ...models import *
from ..agent.load_agent import load_agent
from .chain import execute_chain, load_executor

router = APIRouter()

def callback(*args, **kwargs):
    print(args, kwargs)


@router.post('/llm')
def get_llm_config(db: Session = Depends(get_db)):
    """获取llm配置"""
    llm_config = db.query(LLMConfig).order_by(LLMConfig.model_provider).all()
    return llm_config




@router.post('/{id}/v1/chat/completions')
async def chat(id:str, 
                request: Request, 
                   db: Session = Depends(get_db), 
                   current_user: dict = Depends(get_current_user)):
    """问答入口"""
    # 获取输入数据
    params = await request.json()
    user_id = current_user['user_id']
    
    # agent配置
    agent_config = params.get('config', {})
    # 上下文配置
    context = agent_config.get('context', {})
    context_compress_strage = context.get('memory_recall', 'keep_last')
    max_context_len = context.get('n', 3)


    # 对agent进行路由
    if id == '1':
        # 调用chat_chain 
        agent_executor = load_executor(**agent_config)
    elif id == '2':
        # 调用create_agent助手
        pass
    else:
        # 调用保存的agent
        agent_executor = load_agent_from_db(id, db)

    messages = params['messages']

    if params.get('conversation_id'):
        conversation_id = params.get('conversation_id')
        return conversation_chat(agent_executor, conversation_id, user_id, messages[0], context_compress_strage, max_context_len, db)

    else:
        input = messages.pop(-1)
        # 输入
        messages = [convert_dict_to_message(r) for r in params['messages']]
        return api_chat_complete(input, messages, agent_executor)

        
def load_agent_from_db(agent_id: str, db: Session):
    agent_config = db.query(Agent).filter_by(id=agent_id).first()
    if not agent_config:
        raise HTTPException(status_code=404, detail="Agent not found")
    return load_agent(agent_config, db)


def conversation_chat(agent_executor, conversation_id, user_id, question, context_compress_strage, max_context_len, db):
    """问答入口
    params:
        conversation_id 对话id
        stream 是否使用流的方式输出内容，默认为：True
        max_context_len 最大上下文长度，默认为：3
        context_compress_strage 上下文压缩策略，'keep_last' or 'rag' or 'summary'，默认为：'keep_last'
        user_id: 用户ID
    """
    conversation = db.query(Conversation).filter_by(id=conversation_id).first()

    if not conversation:
        conversation = Conversation(user_id=user_id, id=conversation_id)
        db.add(conversation)
        db.commit()
       
    prompt_embedding = embeddings_model.embed_query(question['content'])
    messages = load_context_message(context_compress_strage, conversation_id, max_context_len, prompt_embedding, user_id, db)
    messages = [{"content": msg.content, "role": msg.role} for msg in messages]
    messages = [convert_dict_to_message(message) for message in messages]
 
    new_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        content=question['content'],
        embedding=prompt_embedding,
        role="user"
    )
    db.add(new_message)
    db.commit()

    def insert_answer(output):
        new_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=output,
            embedding=embeddings_model.embed_query(output),
            role="assistant"
        )
        db.add(new_message)
        db.commit()

    return execute_chain(agent_executor, messages, question, insert_answer, stream=True)



def api_chat_complete():
    """
    给api调用的对话
    """
    pass
        



    





    