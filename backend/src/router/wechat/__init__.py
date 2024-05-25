from fastapi import APIRouter, Depends
from fastapi import Request
import os

from .wechat import check_signature
from .wechat import trans_xml_to_dict, parse_subscribe, mk_res_xml
from pydantic import BaseModel
from ...database import get_db, get_redis_conn
from fastapi import APIRouter


# 定义router
router = APIRouter()

@router.get('/wechat/{appid}')
def check_url(appid: str, request: Request):
    """首次域名验证"""
    params = dict(request.query_params)
    if appid == 'index':
        token = os.environ.get('APP_TOKEN')
        print(token)
        check_str = check_signature(token, params)
    print(check_str)
    return str(check_str)


@router.post('/wechat/{appid}')
async def handle_msg(appid, request: Request, db=Depends(get_db), redis_conn=Depends(get_redis_conn)):
    """处理消息"""
    data = await request.body()  # 异步获取请求体数据
    assert data, '请求数据为空'
    if appid == 'index':
        # 本地服务器验证
        index_handle(data, db, redis_conn)
    else:
        pass 


def index_handle(data, db, redis_conn):
    """当前主服务的微信公众号消息处理"""
    # 解析数据
    post_data = trans_xml_to_dict(data)
    # 事件处理
    if post_data.get('Event'):
        if post_data.get('Event') == u'subscribe' or post_data.get('Event') == u'SCAN':
            # 关注事件处理
            return parse_subscribe(post_data, db, redis_conn)
        
    #     elif post_data.get('Event') == u'unsubscribe':
    #         # 取消关注事件处理
    #         return parse_unsubscribe(post_data)
    #     elif post_data.get('Event') == u'CLICK':
    #         # 点击事件处理
    #         return parse_click(post_data)
    else:
        # 消息处理
        print(post_data)
        # return parse_msg(post_data)  
        res_str = mk_res_xml(post_data, '欢迎关注！')
        print(res_str)
        return res_str
    
# Pydantic模型定义
class TempQrCodeRequest(BaseModel):
    scene_id: int
