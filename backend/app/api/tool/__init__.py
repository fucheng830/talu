from .request_context_tool import context_tools


from fastapi import Request, APIRouter
from fastapi import Depends, HTTPException
import json


from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain.adapters.openai import convert_dict_to_message
from ..common.auth import get_current_user
from ..sse_format import sse_json
from sse_starlette.sse import EventSourceResponse

# 对话路由接口
from langchain_community.adapters.openai import convert_dict_to_message
from ...models import *


from ...database import get_db
from ...models import *


router = APIRouter()



@router.post('/tools')
async def get_tools(
               db: Session = Depends(get_db), 
               current_user: dict = Depends(get_current_user)):
    """"""
    user_id = current_user['user_id']
    tools = db.query(ToolConfig).all()
    return tools









        



    





    