from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, Request

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import requests
import time
from decimal import Decimal

from .auth import get_current_user
from ..schemas import *
from ..models import *
from ..database import get_db
from ..utils import *

router = APIRouter()



# @router.post("/plans/")
# async def create_plan(plan: Plan, db: Session = Depends(get_db)):
#     db.add(plan)
#     db.commit()
#     return {"status": "Plan created"}

# @router.post("/discounts/")
# async def add_discount(discount: Discount, db: Session = Depends(get_db)):
#     db.add(discount)
#     db.commit()
#     return {"status": "Discount added"}


@router.post('/check_order')
async def check_project_order(params: OrderRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    检查订单状态接口
    """
    order_record = db.query(Order).filter_by(order_id=params.order_id).first()
    if order_record:
        if order_record.status == 'paid':
            plan = db.query(Plan).filter_by(id=order_record.plan_id).first()
            user = db.query(User).filter_by(user_id=order_record.user_id).first()
            data = {'status': order_record.status, 'plan': plan.name, 'vip_end_time': user.vip_end_time}
            return data
        else:
            return {'status': order_record.status} 
    else:
        raise HTTPException(status_code=404, detail="未查询到有效的订单")
    
    
def validate_signature(data: dict, pubkey: str) -> bool:
    # 这里需要一个实际的函数来验证微信的签名
    pass


@router.post('/wechat_pay/payback')
async def wechat_pay_callback(request: Request, db: Session = Depends(get_db)):
    """微信支付回调函数"""
    # 读取请求体中的XML数据
    xml_str = await request.body()
    data = trans_xml_to_dict(xml_str.decode('utf-8'))

    # # 验证签名确保请求是从微信发来的
    # if not validate_signature(data, os.environ.get('WECHAT_PUBKEY')):
    #     raise HTTPException(status_code=400, detail="Invalid signature")
    return update_order_status_and_user(data, db)



def update_order_status_and_user(data: dict, db: Session):
    # 获取商户订单号
    out_trade_no = data.get('out_trade_no')
    # 更新订单状态
    order = db.query(Order).filter_by(order_id=out_trade_no).first()
    user = db.query(User).filter_by(user_id=order.user_id).first()
    if order:
        order.status = 'paid'
        order.updated_at = datetime.now()
        user.vip_end_time = order.vip_end_time
        # 检查是否有返利
        # 支付成功后，查看他是否有推荐人
        if user.referee:
            # 如果有推荐人，给推荐人增加返利
            # 假设返利比例是支付金额的10%
            rebate_ratio = Decimal(os.environ.get('REBATE_RATIO', '0.1'))  # 默认值为 0.1
            rebate = order.price * rebate_ratio  # 这里order.price 应该已经是 Decimal 类型
            # 创建返利记录
            rebate_record = Rebate(
                referrer_id=user.user_id,
                beneficiary_id=user.referee,
                order_id=order.order_id,
                rebate_amount=rebate,
                status='success'
            )
            db.add(rebate_record)
        db.commit()
        # 回复微信服务器
        return 'SUCCESS'
    else:
        raise HTTPException(status_code=404, detail="Order not found")
    

@router.get("/rebates/{user_id}")
async def get_rebates(user_id: uuid.UUID, db: Session = Depends(get_db)):
    rebates = db.query(Rebate).filter(Rebate.referrer_id == user_id).all()
    if not rebates:
        return {"status": "No rebates found"}
    return {"status": "Success", "data": [dict(rebate_id=r.id, amount=r.rebate_amount, status=r.status, created_at=r.created_at, paid_at=r.paid_at) for r in rebates]}


@router.post("/withdraw/{user_id}")
async def withdraw_rebate(user_id: uuid.UUID, rebate_id: int, db: Session = Depends(get_db)):
    rebate = db.query(Rebate).filter(Rebate.id == rebate_id, Rebate.referrer_id == user_id).first()
    if not rebate:
        raise HTTPException(status_code=404, detail="Rebate not found")
    if rebate.status != "pending":
        raise HTTPException(status_code=400, detail="Rebate is not in a withdrawable state")
    # 在实际应用中，这里将调用支付系统的API进行提现处理
    # 模拟提现处理
    rebate.status = "paid"
    rebate.paid_at = datetime.utcnow()
    db.commit()
    return {"status": "Withdrawal processed", "rebate_id": rebate_id}


@router.get("/total_rebates/{user_id}")
async def get_total_rebates(user_id: uuid.UUID, db: Session = Depends(get_db)):
    total_rebate = db.query(func.sum(Rebate.rebate_amount)).filter(Rebate.referrer_id == user_id, Rebate.status == "pending").scalar()
    if total_rebate is None:
        total_rebate = 0  # 当没有待提取的返利时，返回0
    return {"status": "Success", "total_rebates": total_rebate}


def wechat_pay(
  out_trade_no=None, 
  total_free=1, 
  spbill_create_ip='127.0.0.1',
  trade_type='MWEB',
  openid=None,
  appid=None,
  mch_id=None,
  body=None,
  notify_url=None,
  scene_info=None,
  pub_key=None
  ):
    """请求下单接口
    """
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    default =  {
    'appid':appid, #公众账号id
    'mch_id':mch_id,# 商户号
    'nonce_str':'',# 随机字符串
    'body':body,#商品描述
    'out_trade_no':out_trade_no, #商户订单号
    'total_fee':total_free, #标价金额
    'spbill_create_ip':spbill_create_ip, #终端ip
    'notify_url':notify_url,
    'trade_type':trade_type,
    'openid':openid,
    'scene_info':scene_info
    }
    headers = {"Content-Type": "application/xml"}
    # 随机字符串
    nonce_str = rand_str()
    default['nonce_str'] = nonce_str
    # 签名
    temp_str = dict_to_url(default)
    temp_str = "{}&key={}".format(temp_str, pub_key)
    sign = mk_sign(temp_str)   
    default['sign'] = sign
    xml_str = trans_dict_to_xml(default)
    res = requests.post(url, data=xml_str.encode('utf-8'), headers=headers)
    return trans_xml_to_dict(res.content)


@router.post('/wechat_pay')
async def wechat(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """创建支付订单 
    """        
    client_ip = request.headers.get("x-forwarded-for")
    if client_ip:
        # 可能有多个IP（如果经过多个代理），取第一个
        client_ip = client_ip.split(",")[0]
    else:
        # 直接连接，没有代理，获取连接方的IP
        client_ip = request.client.host

    params = await request.json()

    user_id = current_user['user_id']
    user = db.query(User).filter_by(user_id = user_id).first()
    plan = db.query(Plan).filter(Plan.id == params['plan_id']).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    price = 0.01 if os.environ.get('PAY_DEBUG') else plan.base_price

    body = plan.name
    trade_type = params['trade_type']
    order_id = params['order_id']
    user_ip = client_ip

    scene_info = {
        "h5_info": {"type":"Wap","wap_url": "http://123qiming.com","wap_name": "趣比特科技"}
                  }
    
    appid = os.environ['WECHAT_APPID']
    mch_id = os.environ['WECHAT_PAY_JSAPI_MCH_ID']
    pub_key = os.environ.get('WECHAT_PUBKEY')
    if trade_type=='JSAPI':
        openid = user.openid
    else:
        openid = None
    
    order_params = dict(
        out_trade_no=order_id,
        total_free=int(price*100),
        spbill_create_ip=user_ip,
        trade_type = trade_type,
        openid=openid,
        appid=appid,
        mch_id=mch_id,
        body=body,
        notify_url='{}/wechat_pay/payback'.format(os.environ['STATIC_URL']),
        scene_info=scene_info,
        pub_key=pub_key
    )
    print(order_params)
    res = wechat_pay(
            **order_params
    )

    if user.vip_end_time and user.vip_end_time > datetime.now():
        start_date = user.vip_end_time
    else:
        start_date = datetime.now()

    end_date = start_date + timedelta(days=plan.expire_days)
    
    order = Order(
        order_id=order_id,
        user_id=user_id,
        plan_id=plan.id,
        trade_type=trade_type,
        price=price,
        status='unpaid',
        created_at=datetime.now(),
        updated_at=datetime.now(),
        vip_end_time=end_date,
        pay_info=res
        )
    db.add(order)
    db.commit()

    if trade_type=='JSAPI':
        print(res)
        res = {'appId':res['appid'], 'timeStamp':str(time.time())[:10], 'nonceStr':rand_str(), 'package':f'prepay_id={res["prepay_id"]}', 'signType':'MD5'}
        temp_str = dict_to_url(res)
        sign = mk_sign("{}&key={}".format(temp_str, pub_key))
        res['paySign'] = sign

    return res


@router.post("/withdraw")
async def withdraw(amount: Decimal, user_id: uuid.UUID, db: Session = Depends(get_db)):
    # 检查提现金额是否有效
    if amount <= Decimal('0.00'):
        raise HTTPException(status_code=400, detail="Invalid amount")

    # 在数据库中查找用户
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.cash_balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # 校验cash_balance>=amount
    if user.cash_balance >= amount:
        # 创建提现记录
        new_withdrawal = Withdrawal(
            user_id=user_id,
            amount=amount,
            status='pending',
            requested_at=datetime.now()
        )
        db.add(new_withdrawal)
        user.cash_balance -= amount
        db.commit()
        return {"status": "Success", "message": "Withdrawal request submitted"}
    else:
        raise HTTPException(status_code=400, detail="Insufficient funds")