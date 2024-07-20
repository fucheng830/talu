from fastapi import FastAPI, Request, Response, APIRouter
from fastapi import Depends, HTTPException
import json
import requests
import time

import os
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain.agents import tool

from langchain.callbacks.base import BaseCallbackHandler
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.agents import Tool
from langchain.agents import AgentExecutor, tool

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.adapters.openai import convert_dict_to_message
from langchain.adapters.openai import convert_message_to_dict
from fastapi.responses import StreamingResponse
from ..common.auth import get_current_user
import re
from ..sse_format import sse_json
from sse_starlette.sse import EventSourceResponse

from ...database import get_db, set_key, get_key
from ...models import *
from ..tool import context_tools

from langchain.tools.render import format_tool_to_openai_function
from langchain_community.adapters.openai import convert_openai_messages
from ..agent.load_agent import load_agent
from ...schemas import ConversationRequest
from typing import List, Dict
from sqlalchemy import desc

router = APIRouter()

class ManageContext:
    def __init__(self, db, user):
        self.db = db
        self.user = user

    async def update_tokens(self):
        new_token_count = self.user.user_info.get('usable_token', 0) - 1  # 假设每次对话消耗1个token
        # self.user.user_info['usable_token'] = new_token_count
        # self.db.query(User).filter_by(user_id=self.user.user_id).update({'user_info': self.user.user_info})
        # self.db.commit()
        print('Tokens updated:', new_token_count)


def check_vip_limit(user_id, limit=100):
    """检查vip模型是否可用"""
    dt = datetime.now().strftime('%Y%m%d')
    key = f'plus_{user_id}_{dt}'
    used_num = get_key(key)
    if used_num is None:
        used_num = 0
        used_num +=1
        set_key(key, used_num, ex=60*60*24)
        
    else:
        used_num = int(used_num)
        if used_num<=limit:
            used_num+=1
            set_key(key, used_num, ex=60*60*24)
        else:
            return False
    return True


async def check_user_permissions(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user['user_id']
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户未注册")
    
    if user.vip_end_time is not None and user.vip_end_time < datetime.now():
        raise HTTPException(status_code=401, detail="会员已过期")

    elif user.vip_end_time is None:
        usable_token = user.user_info.get('usable_token', 0)
        if usable_token <= 0:
            raise HTTPException(status_code=429, detail="您的可用对话次数不足，请订阅会员")
        else:
            user.user_info['usable_token'] -= 1
            db.query(User).filter_by(user_id=user_id).update({'user_info': user.user_info})
            db.commit()
    
    if not check_vip_limit(user_id):
        raise HTTPException(status_code=429, detail="您的VIP模型使用次数已经用完，请明天再试")

    return user



def load_executor(model, db):
    """加载模型执行器"""
    model_config = db.query(Agent).filter_by(id=model).first()
    if model_config is not None:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", model_config.system_prompt),
            MessagesPlaceholder("msgs"),
            ("user", "{input_text}"),
        ])
        llm = ChatOpenAI(**model_config.llm)
        agent_executor = prompt_template | llm
        return agent_executor, model_config
    else:
        raise ValueError("Model not found")


def get_last_messages(conversation_id: uuid.UUID, max_context_len: int, user_id:uuid.UUID, db: Session):
    messages = db.query(Message).filter_by(conversation_id=conversation_id, user_id=user_id).order_by(desc(Message.created_at)).limit(max_context_len).all()
    return messages[::-1]  # Reverse to maintain chronological order


def summarize_messages(conversation_id: uuid.UUID, max_context_len: int, user_id:uuid.UUID, db: Session):
    # 简单的消息汇总实现，实际中可以用更复杂的算法
    conversation = db.query(Conversation).filter_by(conversation_id=conversation_id, user_id=user_id).first()
    summary = conversation.summary 
    return summary


def rag_search(conversation_id: uuid.UUID, max_context_len: int, user_id:uuid.UUID, db: Session):
    # 简单的向量搜索实现，实际中应该使用向量数据库或嵌入技术
    # 这里仅示例返回前 max_context_len 个消息
    pass 
    

def process_context_compression(strategy: str, conversation_id: uuid.UUID, max_context_len: int, user_id:uuid.UUID, db: Session) -> List[Dict]:
    """上下文压缩"""
    if strategy == 'keep_last':
        return get_last_messages(conversation_id, max_context_len, user_id, db)
    elif strategy == 'summary':
        summary = summarize_messages(conversation_id, max_context_len, user_id, db)
        return [{"content": summary, "role": "user"}]
    elif strategy == 'rag':
        return rag_search(conversation_id, max_context_len, user_id, db)
    else:
        raise ValueError("Invalid context_compress_strage value")


def load_context_message(strategy, conversation_id, max_context_len, user_id, db):
    """加载上下文消息"""
    messages_len = db.query(Message).filter_by(conversation_id=conversation_id, user_id=user_id).count()
    if messages_len > max_context_len:
        messages = process_context_compression(strategy, conversation_id, 3, user_id, db)
    else:
        messages = db.query(Message).filter_by(conversation_id=conversation_id, user_id=user_id).all()
    return messages

async def stream_chat(agent_executor, messages, input_text):
    try:
        async for chunk in agent_executor.astream(
            {"input_text": input_text,
            "msgs": [convert_dict_to_message(message) for message in messages]}
        ):
            if chunk:
                row_data = sse_json(chunk.content)
                yield json.dumps(row_data)
    finally:
        yield json.dumps(sse_json('', finish_reason='stop'))
        

def execute_chain(agent_executor, messages, input_text, user_id, db, stream=True):
    if stream:
        return EventSourceResponse(stream_chat(agent_executor, messages, input_text), media_type="text/event-stream")
    else:
        output = agent_executor.invoke(
            {"input": input_text,
            "chat_history": [convert_dict_to_message(message) for message in messages]}
        )
        return sse_json(output['output']) 


@router.post('/conversation/talk')
async def talk(params: ConversationRequest, db: Session = Depends(get_db), user: User = Depends(check_user_permissions)):
    """问答入口
    prompt 提问的内容。
    model 对话使用的模型，通常整个会话中保持不变。
    message_id 消息ID，通常使用str(uuid.uuid4())来生成一个。
    parent_message_id 父消息ID，首次同样需要生成。之后获取上一条回复的消息ID即可。
    conversation_id 首次对话可不传。ChatGPT回复时可获取。
    stream 是否使用流的方式输出内容，默认为：True
    max_context_len 最大上下文长度，默认为：3
    context_compress_strage 上下文压缩策略，'keep_last' or 'rag' or 'summary'，默认为：'keep_last'
    search_config 搜索配置，用于搜索引擎
    """
    messages = load_context_message(params.context_compress_strage, params.conversation_id, params.max_context_len, user.user_id, db)
    agent_executor, model_config = load_executor(params.model, db)
    # messages 增加系统消息
    # messages.insert(0, {"content": model_config.system_prompt, "role": "system"})
    return execute_chain(agent_executor, messages, params.prompt, user.user_id, db, params.stream)
    



@router.post('/conversation/gen_title')
async def gen_title(request: Request):
    """修改对话的标题"""
    data = await request.json()
    messages = data['messages']
    contents = ['{}: {}'.format(message['role'], message['content']) for message in messages]
    prompt = """
    你是一个bot，你的任务是生成一个标题，这个标题是对以下对话的总结。
    {}
    请按照以下要求返回对话标题。
    1、请直接输出对话标题。
    2、尽量简洁明了。
    3、尽量包含对话的主要内容。
    4、尽量包含对话的亮点。
    5、尽量包含对话的结论。
    6、不要出现标点符号。
    """.format('\n'.join(contents))
    llm = ChatOpenAI(model="v1", 
                     temperature=0, 
                     streaming=False
                     )
    title = llm.predict(prompt)
    return {'status':'Success', 'data':title}





    