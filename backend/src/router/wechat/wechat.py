from pydantic import BaseModel
from typing import Optional
import hashlib
import os

from fastapi import Request, Depends

from bs4 import BeautifulSoup
from .api import WeChat
from ...models import User
import hashlib
import time 
import random

def sha1(str):
    return hashlib.sha1(str.encode("utf-8")).hexdigest()


def check_signature(token, params):
    """微信公众号首次验证域名，检查签名"""
    tmp_arr = [token, params['timestamp'], params['nonce']]
    tmp_arr.sort()
    tmp_str = "".join(tmp_arr)
    tmp_str = sha1(tmp_str)
    if tmp_str==params['signature']:
        if 'echostr' in params:
            return params['echostr']
        return 'true' 
    else:
        return 'false'


def trans_xml_to_dict(xml):
    """
    将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象
    
    :param xml: 原始 XML 格式数据
    :return: dict 对象
    """
    soup = BeautifulSoup(xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}
    
    # 将 XML 数据转化为 Dict
    data = dict([(item.name, item.text) for item in xml.find_all()])
    return data


def mk_res_xml(res, content):
    """生成回复消息的 XML 格式数据"""
    res_text = '''
<xml>
  <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
  <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
  <CreateTime>{CreateTime}</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[{Content}]]></Content>
</xml>
'''.format(ToUserName=res['FromUserName'], FromUserName=res['ToUserName'], Content=content, CreateTime=str(int(time.time()))[:8])
    return res_text




# 实现不同的解析函数
def parse_msg(data):
    """消息处理"""
    pass

def parse_click(data):
    """点击事件处理"""
    pass

def parse_unsubscribe(data):
    """取消关注事件处理"""
    pass

def parse_subscribe(post_data, db, redis_conn):
    print(post_data)
    """关注事件处理"""
    # 获取用户 OpenID
    openid = post_data['FromUserName']
    # 获取用户信息
    wc = WeChat(os.environ['APP_ID'], os.environ['APP_SECRET'])
    user_info = wc.get_user_info(openid)
    print(user_info)
    event_key = post_data.get('EventKey')
    if event_key:
        event_key = event_key.strip()
        event_key = event_key.split('_')[-1]
        if event_key:
            qr_scene = int(event_key)
            user = db.session.query(User).filter(User.openid==openid).first()
            if user:
                # 已经存在账号，给予通过验证, 并设置过期时间
                redis_conn.set(qr_scene, user.userId, ex=60*60)
            else:
                # 不存在账号，创建账号
                userId = int(time.time()*1000)
                user = User(
                    openid=user_info['openid'], 
                    userId=userId, name='用户'+str(random.randint(1000, 9999)), 
                    union_id=user_info['unionid'])
                db.session.add(user)
                db.session.commit()
                # 保存到redis
                redis_conn.set(qr_scene, userId, ex=60*60)

            return mk_res_xml(post_data, '登录成功！')
            
    return mk_res_xml(post_data, '欢迎关注！')
