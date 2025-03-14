from typing import Dict, List, Optional
from uuid import UUID
from ..models import Agent, ToolConfig
from sqlalchemy.orm import Session

class AgentService:
    def __init__(self, db: Session):
        self.db = db

    async def create_agent(self, agent_data: Dict) -> Agent:
        agent = Agent(**agent_data)
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        return agent

    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.db.query(Agent).filter(Agent.id == agent_id).first()

    async def list_agents(self, user_id: str) -> List[Agent]:
        return self.db.query(Agent).filter(Agent.user_id == user_id).all()

    async def update_agent(self, agent_id: str, agent_data: Dict) -> Optional[Agent]:
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if agent:
            for key, value in agent_data.items():
                setattr(agent, key, value)
            self.db.commit()
            self.db.refresh(agent)
        return agent

    async def delete_agent(self, agent_id: str) -> bool:
        agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if agent:
            self.db.delete(agent)
            self.db.commit()
            return True
        return False
