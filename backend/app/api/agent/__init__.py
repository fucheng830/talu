# 导入所需的模块和库
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from langchain.agents import Tool
from ..common.auth import get_current_user
from ...schemas import AgentBase
from ...schemas import AgentQuery
from ...models import *
from ...database import get_db

# 创建一个新的APIRouter实例
router = APIRouter()

@router.post('/agent_edit')
def add_agent(agent: AgentBase, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    添加或更新代理(agent)信息。
    如果代理已经存在，则更新其信息；否则，创建一个新的代理。
    """
    agent_dict = agent.model_dump()
    agent_obj = Agent(**agent_dict, user_id=current_user.get('user_id'))
    # 查询是否已经存在agent
    agent_exist = db.query(Agent).filter_by(id=agent_dict['id'], user_id=current_user.get('user_id')).first()
    if agent_exist:
        # 更新agent
        for key in agent_dict:
            if agent_dict[key] != getattr(agent_exist, key):
                setattr(agent_exist, key, agent_dict[key])
  
        db.commit()
        db.refresh(agent_exist)
        return agent_exist
    else:
        # 添加新的agent
        db.add(agent_obj)
        db.commit()
        db.refresh(agent_obj)
        return agent_obj


@router.post('/agents')
def get_agents(db: Session = Depends(get_db)):
    """
    获取所有公共代理(agent)的信息，按类别分类。
    返回每个类别下的代理列表，最多返回20个代理。
    """
    datas = {}
    categories = db.query(AgentCategory).all()
    for category in categories:
        agents = db.query(Agent).filter_by(category=category.name, permission='public').limit(20).all()
        datas[category.name] = [{'id':r.id, 'name':r.name, 'description':r.description, 'avatar':r.avatar} for r in agents]

    keys = list(datas.keys())

    all_data = []
    for key in keys:
        row = {'label':key, 'children':datas[key]}
        all_data.append(row)
    data = {'categories':keys, 'agents':all_data}
    return {'status':'Success', 'message':'获取成功', 'data':data}


@router.post('/my_agents')
def get_my_agents(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    获取当前用户自己创建的代理(agent)列表。
    返回所有非临时的代理信息。
    """
    datas = {}
    agents = db.query(Agent).filter(Agent.user_id==current_user['user_id'], Agent.permission!='temp').all()
    return agents


@router.post('/agent')
def get_agent(agent_query: AgentQuery, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    获取单个代理(agent)的信息。
    根据代理ID和权限（用户自己的代理或公共代理）进行查询。
    """
    from sqlalchemy import or_, and_
    agent = db.query(Agent).filter(
    or_(
        # 第一组条件
        and_(Agent.id == agent_query.id, Agent.user_id == current_user['user_id']),
        # 第二组条件
        and_(Agent.id == agent_query.id, Agent.permission == 'public')
    )
    ).first()
    if agent:
        return agent
    else:
        raise HTTPException(status_code=400, detail="Agent not found")


def update_agent():
    """
    更新代理(agent)的功能。
    目前该功能未实现。
    """
    pass


@router.post('/delete_agent')
def delete_agent(agent_query: AgentQuery, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    删除代理(agent)。
    只能删除当前用户自己创建的代理。
    """
    agent = db.query(Agent).filter_by(id=agent_query.id, user_id=current_user['user_id']).first()
    if agent:
        db.delete(agent)
        db.commit()
        return {'status':'Success', 'message':'删除成功'}
    else:
        raise HTTPException(status_code=400, detail="Agent not found")


@router.post('/search_agent')
def search_agent(query: str, db: Session = Depends(get_db)):
    """
    根据名称搜索公共代理(agent)。
    使用模糊查询返回匹配的代理列表。
    """
    agents = db.query(Agent).filter(Agent.name.ilike(f"%{query}%"), Agent.permission == 'public').all()
    return agents
