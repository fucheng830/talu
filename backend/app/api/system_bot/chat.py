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


async def app_chat(agent_id:str, 
                   agent_type:str, 
                   request: Request, 
                   db: Session = Depends(get_db), 
                   current_user: dict = Depends(get_current_user)):
    """问答入口"""
    # 检查用户是否有权限
    user_id = current_user['user_id']
    user = db.query(User).filter_by(user_id=user_id).first()
    if user:
        if user.vip_end_time is not None and user.vip_end_time<datetime.now():
            raise HTTPException(status_code=401, detail="会员已过期")
        
        elif user.vip_end_time is None:
            usable_token = user.user_info.get('usable_token', 0)
            if usable_token<=0:
                raise HTTPException(status_code=429, detail="您的可用对话次数不足，请订阅会员")
            else:
                user.user_info['usable_token'] -= 1
                db.query(User).filter_by(user_id=user_id).update({'user_info': user.user_info})
                db.commit()

    else:
        raise HTTPException(status_code=401, detail="用户未注册")
    
    # 检查是否已经使用完当日额度
    if not check_vip_limit(user_id):
        raise HTTPException(status_code=429, detail="您的VIP模型使用次数已经用完，请明天再试")
    
    data = await request.json()
    messages = data['messages']



        
        





    






    