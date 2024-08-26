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
    messages = [convert_dict_to_message(message) for message in messages]
    return conversation_chat(agent_executor, user_id, messages, db)

        
def load_agent_from_db(agent_id: str, db: Session):
    agent_config = db.query(Agent).filter_by(id=agent_id).first()
    if not agent_config:
        raise HTTPException(status_code=404, detail="Agent not found")
    return load_agent(agent_config, db)


import time

def conversation_chat(agent_executor, user_id, messages, db):
    """问答入口
    params:
        stream 是否使用流的方式输出内容，默认为：True
        user_id: 用户ID
    """
    # 定义插入答案的函数
    def insert_answer(output):
        print('output:', output)
        # start_time = time.time()

        # new_message = Message(
        #     user_id=user_id,
        #     content=output,
        #     role="assistant"
        # )
        # db.add(new_message)
        # db.commit()
        # insert_assistant_message_time = time.time() - start_time
        # print(f"插入助手消息时间: {insert_assistant_message_time:.4f}秒")

    # 执行链
    
    result = execute_chain(agent_executor, messages, insert_answer, stream=True)
    return result




        



    





    