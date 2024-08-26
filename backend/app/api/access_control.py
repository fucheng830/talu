# 接口付费，及套餐计算模块
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ...database import get_db, set_key, get_key
from ...models import User

class AccessControl:
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
        self.user = self.get_user()

    def get_user(self):
        user = self.db.query(User).filter_by(user_id=self.user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="用户未注册")
        return user

    def check_membership(self):
        if self.user.vip_end_time is not None and self.user.vip_end_time < datetime.now():
            raise HTTPException(status_code=401, detail="会员已过期")

    def check_token(self):
        usable_token = self.user.user_info.get('usable_token', 0)
        if usable_token <= 0:
            raise HTTPException(status_code=429, detail="您的可用对话次数不足，请订阅会员")
        else:
            self.user.user_info['usable_token'] -= 1
            self.db.query(User).filter_by(user_id=self.user_id).update({'user_info': self.user.user_info})
            self.db.commit()

    def check_vip_limit(self, limit=100):
        dt = datetime.now().strftime('%Y%m%d')
        key = f'plus_{self.user_id}_{dt}'
        used_num = get_key(key)

        if used_num is None:
            used_num = 0
            used_num += 1
            set_key(key, used_num, ex=60 * 60 * 24)
        else:
            used_num = int(used_num)
            if used_num < limit:
                used_num += 1
                set_key(key, used_num, ex=60 * 60 * 24)
            else:
                raise HTTPException(status_code=429, detail="您的VIP模型使用次数已经用完，请明天再试")

def access_control(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """权限控制依赖"""
    user_id = current_user['user_id']
    access_control = AccessControl(db, user_id)
    access_control.check_membership()
    access_control.check_token()
    access_control.check_vip_limit()

"""

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from .access_control import access_control

router = APIRouter()

# 使用示例
@router.post("/chat/{agent_id}/{agent_type}")
async def app_chat(agent_id: str, 
                   agent_type: str, 
                   request: Request, 
                   db: Session = Depends(get_db), 
                   current_user: dict = Depends(get_current_user),
                   _ = Depends(access_control)):  # 使用权限控制依赖
    data = await request.json()
    messages = data['messages']
"""