from fastapi import HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter
import uuid
from ..database import get_db, get_redis_conn, get_key, set_key
from ..models import User, UserThirdPartyAccount
from .auth import create_access_token
from ..schemas import *
from ..utils import md5, to_dict
from .send_mail import send
import random
import time
import logging
from typing import Optional
import redis
from random import randint
import requests
import os


"""
用户模块
 - 登录
    - 邮箱密码登录
    - 第三方登录
 - 注册
    - 检查邮箱是否已经被注册
    - 发送验证码
    - 注册
    - 绑定第三方账号
"""

logger = logging.getLogger(__name__)

router = APIRouter()

# Define the Pydantic model for the request body
class LoginData(BaseModel):
    email: str
    password: str

# Optional: Define a Pydantic model for the user info response
class UserInfo(BaseModel):
    userId: int
    access_token: str
    # include other user fields but exclude the password


class RegisterData(BaseModel):
    email: str
    password: str
    emailCode: str
    referee: Optional[str] = None


class EmailData(BaseModel):
    email: str


def v_code():
    """生成验证码"""
    import random
    code = []
    for i in range(4):
        add = random.choice(range(10))
        code.append(str(add))

    return ''.join(code)


def _check_refree(refree, db):
    """检查推荐人"""
    try:
        if refree:
            # 查询User表，找到具有给定userId的用户
            _m = db.query(User).filter_by(user_id=refree).first()
            if _m:
                # 更新推荐人的余额
                _m.user_info = {'usable_token':_m.user_info['usable_token'] + 50}
                db.commit()
            else:
                # 如果找不到用户，则返回None
                return None
        else:
            # 如果未提供refree，则返回None
            return None
    except Exception as e:
        # 记录执行此函数时发生的任何异常
        logger.error(e)

def get_qy_access_token(redis_conn):
    # 获取 access_token 的代码
    import requests
    import os
    AppId = os.environ.get("CORP_ID")
    AppSecret = os.environ.get("CORP_SECRET")
    WECHAT_SERVICE_URL = os.environ.get("WECHAT_SERVICE_URL")
    res = requests.post(f'{WECHAT_SERVICE_URL}/token', json={'appid':AppId, 'secret':AppSecret})
    return res.content.decode('utf-8')


@router.post('/login')
def login(login_data: LoginData, db: Session = Depends(get_db)):
    """登录"""
    password_hash = md5(login_data.password)
    user = db.query(User).filter_by(email=login_data.email, password=password_hash).first()
    
    if user:
        del user.password
        user.access_token = create_access_token({"user_id":str(user.user_id), "password":login_data.password})
        return {'status': 'Success', 'message': '登录成功', 'data': user}
    else:
        raise HTTPException(status_code=400, detail='账号或密码错误')
    

@router.post('/register')
def register(register_data: RegisterData, db: Session = Depends(get_db), redis_conn=Depends(get_redis_conn)): 
    """注册""" 
    _m = db.query(User).filter_by(email=register_data.email).first()  # 查询数据库，检查邮箱是否已经被注册
    if _m:  
        # 如果邮箱已经被注册
        return {'status': 'Fail', 'message': '邮箱已经被注册', 'data': 0} # 返回失败信息
    else:  # 如果邮箱未被注册
        check_code = redis_conn.get(register_data.email)  # 从Redis中获取验证码
        if not check_code:  # 如果验证码不存在（已过期）
            return {'status': 'Fail', 'message': '验证码已经过期', 'data': 0} # 返回失败信息
        else:  # 如果验证码存在
            if check_code.decode() != register_data.emailCode:  # 检查验证码是否正确
                return {'status': 'Fail', 'message': '验证码错误', 'data': 0}  # 返回失败信息
        
        _check_refree(register_data.referee, db)  # 检查推荐人是否存在
        
        register_data.password = md5(register_data.password)  # 对密码进行加密
        

        user = User(email=register_data.email, 
                    name = '用户'+str(random.randint(1, 99999999)),
                    password=register_data.password, 
                    referee=register_data.referee
                    )  # 创建用户对象
        
        db.add(user)  # 将用户对象添加到数据库会话中
        db.commit()  # 提交数据库会话，保存用户记录
        
        user_info = to_dict(user)  # 将用户对象转换为字典
       
        user_info['access_token'] = create_access_token({"user_id":str(user_info['user_id']), 
                                                         "password":user_info['password']})  # 生成访问令牌
        del user_info['password']  # 删除密码字段
        return {'status': 'Success', 'message': '注册成功', 'data': user_info}  # 返回成功信息和用户信息
    

@router.post("/check_mail")
def check_mail(email_data: EmailData, db: Session = Depends(get_db)):
    _m = db.query(User).filter_by(email=email_data.email).first()
    if _m:
        return {'status': 'Fail', 'message': '邮箱已经被注册', 'data': 0}
    else:
        return {'status': 'Success', 'message': '邮箱可以注册', 'data': 1}


@router.post("/send_code")
def send_code(email_data: EmailData, redis_conn=Depends(get_redis_conn)):
    check_code = v_code()
    redis_conn.set(email_data.email, check_code, ex=60*5)
    access_token = get_qy_access_token(redis_conn)
    send(access_token, email_data.email, check_code)
    return {'status': 'Success', 'message': '邮箱验证码已经发送', 'data': 1}


class ThirdPartyLoginData(BaseModel):
    third_party_name: str
    third_party_user_id: str
    additional_info: Optional[dict] = None


@router.post("/third_party_login")
def third_party_login(login_data: ThirdPartyLoginData, db: Session = Depends(get_db)):
    # 检查是否已经存在一个绑定了这个第三方账号的用户
    existing_account = db.query(UserThirdPartyAccount).filter(
        UserThirdPartyAccount.third_party_name == login_data.third_party_name,
        UserThirdPartyAccount.third_party_user_id == login_data.third_party_user_id
    ).first()

    if existing_account:
        # 如果找到了，获取用户信息
        user = db.query(User).filter(User.user_id == existing_account.user_id).first()
        if user:
            # 生成访问令牌
            access_token = create_access_token({"user_id": str(user.user_id)})
            # 返回用户信息和访问令牌
            return {'status': 'Success', 'message': '登录成功', 'data': {'user_id': user.user_id, 'access_token': access_token}}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        # 如果是第一次使用这个第三方账号登录，创建一个新的用户和第三方账号绑定
        new_user = User(
            name='用户' + str(random.randint(1, 99999999)),
            # 其他必要的用户信息...
        )
        db.add(new_user)
        db.commit()

        new_account = UserThirdPartyAccount(
            user_id=new_user.user_id,
            third_party_name=login_data.third_party_name,
            third_party_user_id=login_data.third_party_user_id,
            additional_info=login_data.additional_info
        )
        db.add(new_account)
        db.commit()

        # 生成访问令牌
        access_token = create_access_token({"user_id": str(new_user.user_id)})
        # 返回新创建的用户信息和访问令牌
        return {'status': 'Success', 'message': '第三方账号登录成功，用户已创建', 'data': {'user_id': new_user.user_id, 'access_token': access_token}}
    

# 确保已经从相应模块导入 User 模型和你数据的 Session 类以及你的redis连接
@router.post('/wechat_scan_callback')
def handle_user_subscription(params: ScannerCallbackBody, 
                             db: Session = Depends(get_db),
                             redis_conn: redis.StrictRedis = Depends(get_redis_conn)) -> str:
    """
    处理用户关注事件。如果用户不存在，则创建新用户；如果用户存在，则进行相应的更新。

    :param openid: 微信用户的OpenID
    :param user_info: 包含用户信息的字典
    :param qr_scene: 二维码场景标识
    :param db: 数据库会话实例
    :return: 响应XML字符串表示用户登陆成功或失败
    """
    print(params.user_info)
    print(params.qr_scene)
    try:
        user = db.query(User).filter(User.openid == params.user_info['openid']).first()
        if user:
            # 用户已存在
            # 在这里可以进行任意的用户更新操作
            # ...
            # 给予通过验证并设置过期时间
            redis_conn.set(params.qr_scene, str(user.user_id), ex=60 * 60)
        else:
            referee = redis_conn.get(f'referee.{params.qr_scene}')
            print(referee)

            if referee is not None:
                referee = referee.decode('utf-8')

            new_user = User(
                openid=params.user_info['openid'],
                name=f'用户{randint(1000, 999999)}',
                union_id=params.user_info.get('union_id'),
                referee=referee
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            # 将新用户保存到Redis并设置过期时间
            redis_conn.set(params.qr_scene, str(new_user.user_id), ex=60 * 60)
        return '用户登陆成功'
    except Exception as e:
        db.rollback()  # 如果出现错误则撤销数据库操作
        logger.error(f'Error handling user subscription: {str(e)}')  # 记录错误日志
        return '用户登录失败！'


@router.post('/scan_qr')
def scan_qr(params: ScanQrParams, redis_conn: redis.StrictRedis = Depends(get_redis_conn)) -> dict:
    """
    扫描二维码，检查用户是否已经关注。

    :param qr_scene: 二维码场景标识
    :param redis_conn: Redis连接实例
    :return: 返回用户ID或者空字符串
    """
    # 微信服务接口
    wechat_url = os.environ.get('WECHAT_SERVICE_URL')
    service_id = os.environ.get('WECHAT_SERVICE_ID')
    url = f'{wechat_url}/{service_id}/scan_qr'

    referee = params.referee or 'none'
    redis_conn.set(f'referee.{params.scene_id}', str(referee), ex=60 * 60)
    res = requests.post(url, json={"scene_id": params.scene_id})
    if res.status_code == 200:
        return res.json()
    

@router.post('/check_wechat_login')
def check_wechat_login(data: ScanQrParams, db: Session = Depends(get_db)):
    """
    检查微信登录

    :param data: 包含用户信息的字典
    :param db: 数据库会话实例
    :return: 包含用户信息的字典
    """
    user_id = get_key(data.scene_id)
    if user_id:
        user = db.query(User).filter_by(user_id=user_id).first()
        if user:
            del user.password
            user.access_token = create_access_token({"user_id":str(user.user_id), "password":user.password})
            return {'status': 'Success', 'message': '登录成功', 'data': user}
        else:
            return {'status': 'Fail', 'message': '账号信息错误'}
    else:
        return {'status': 'Fail', 'message': '未查询到信息'}
    

class WechatLoginData(BaseModel):
    code: str
    referee: Optional[str] = None 

@router.post("/wechat_login")
def wechat_login(data: WechatLoginData, db: Session = Depends(get_db)):
    import json

    APPID = os.environ['WECHAT_APPID']
    SECRET = os.environ['WECHAT_APP_SECRET']

    cache = get_key(data.code)

    if cache:
        access_info = json.loads(cache)
    else:
        url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={APPID}&secret={SECRET}&code={data.code}&grant_type=authorization_code'
        res = requests.get(url)
        if res.status_code == 200:
            access_info = res.json()
            if 'errcode' in access_info:
                raise HTTPException(status_code=400, detail="Login failed")
            set_key(data.code, json.dumps(access_info), ex=60*5)
    
    url = f'https://api.weixin.qq.com/sns/userinfo?access_token={access_info["access_token"]}&openid={access_info["openid"]}&lang=zh_CN'
    res = requests.get(url, headers = {
        'Accept': 'text/plain;charset=UTF-8',
    })
    if res.status_code == 200:
        user_info = res.json()
        user_info['nickname'] = user_info['nickname'].encode('iso-8859-1').decode('utf-8')

        user = db.query(User).filter_by(openid=user_info['openid']).first()
        if user:
            pass
        else:
            # 检查推荐人是否存在，如果存在则更新推荐人的余额
            _check_refree(data.referee, db)

            new_user = User(
                            name=user_info['nickname'], 
                            openid=user_info['openid'], 
                            avatar=user_info['headimgurl'], 
                            referee=data.referee, 
                            union_id=user_info.get('unionid'))
            db.add(new_user)
            db.commit()
            # 刷新new_user
            db.refresh(new_user)
            user = new_user
        
        user_info = to_dict(user)
        user_info['access_token'] = create_access_token({"user_id":str(user_info['user_id']), 
                                                        "password":user_info['password']})  # 生成访问令牌
        del user_info['password']
        return {"status": "Success", "message": "Login successful", "data": user_info}



@router.post("/activation-status/{code}")
async def get_activation_status(code: str):
    if code in activation_codes:
        return activation_codes[code]
    else:
        raise HTTPException(status_code=404, detail="Activation code not found")


@router.post("/create-activation-code/")
async def create_activation_code(code: str):
    if code not in activation_codes:
        activation_codes[code] = ActivationCode(code=code)
        return {"message": "Activation code created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Activation code already exists")
    

@router.post("/activate/")
async def activate_code(code: str, user_id: int, package: str):
    if code in activation_codes:
        if activation_codes[code].is_used:
            raise HTTPException(status_code=400, detail="Activation code already used")
        activation_codes[code].is_used = True
        activation_codes[code].user_id = user_id
        activation_codes[code].package = package
        activation_codes[code].activation_time = datetime.now()
        return {"message": "Activation successful"}
    else:
        raise HTTPException(status_code=404, detail="Activation code not found")




# @router.post("/user", response_model=UserResponse)
# def get_user(user_data: UserData, db: Session = Depends(get_db)):
#     """根据条件获取用户信息"""
#     if user_data.user_id:
#         user = db.query(User).get(user_data.user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="用户不存在")
#         return user
#     elif user_data.search_query:
#         # 根据搜索条件查询用户
#         users = db.query(User).filter(User.name.like(f"%{user_data.search_query}%")).all()
#         return users
#     else:
#         raise HTTPException(status_code=400, detail="无效的请求")


# @router.post("/user/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user_data: UpdateUserData, db: Session = Depends(get_db)):
#     """更新用户信息"""
#     user = db.query(User).get(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="用户不存在")
#     user.name = user_data.name
#     user.email = user_data.email
#     db.commit()
#     return user


# @router.post("/user/{user_id}/delete")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     """删除用户"""
#     user = db.query(User).get(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="用户不存在")
#     db.delete(user)
#     db.commit()
#     return {"message": "用户已删除"}
