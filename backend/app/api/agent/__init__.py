# Agent模块# tools 
# system_prompt
# rag
# llm 

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




router = APIRouter()


@router.post('/agent_edit')
def add_agent(agent: AgentBase, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # 添加agent
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
        db.add(agent_obj)
        db.commit()
        db.refresh(agent_obj)
        return agent_obj


@router.post('/agents')
def get_agents(db: Session = Depends(get_db)):
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
    datas = {}
    agents = db.query(Agent).filter(Agent.user_id==current_user['user_id'], Agent.permission!='temp').all()
    return agents


@router.post('/agent')
def get_agent(agent_query: AgentQuery, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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
    pass


@router.post('/delete_agent')
def delete_agent(agent_query: AgentQuery, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # 删除agent，只能删除自己的agent
    agent = db.query(Agent).filter_by(id=agent_query.id, user_id=current_user['user_id']).first()
    if agent:
        db.delete(agent)
        db.commit()
        return {'status':'Success', 'message':'删除成功'}
    else:
        raise HTTPException(status_code=400, detail="Agent not found")



@router.post('/search_agent')
def search_agent(query: str, db: Session = Depends(get_db)):
    agents = db.query(Agent).filter(Agent.name.ilike(f"%{query}%"), Agent.permission == 'public').all()
    return agents


