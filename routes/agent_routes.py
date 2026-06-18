import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

from database.agent_db import dbagant

logger = logging.getLogger(__name__)

RANK = {"Junior", "Senior", "Commander"}

class CreateAgent(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    specialty: str = Field(..., min_length=1, max_length=50)
    agent_rank: Literal["Junior", "Senior", "Commander"]


class UpdateAgent(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    specialty: str | None = Field(None, min_length=1, max_length=50)
    agent_rank: Literal["Junior", "Senior", "Commander"] | None = None


router = APIRouter(prefix="/agents")

@router.post("", status_code=201)
def create_agent(agent: CreateAgent):
    logger.info(f"Creating agent")
    data = dbagant.create_agent(agent.model_dump())
    if data["agent_rank"] not in RANK:
        logger.warning(f"Illegal rank for agent {agent.name}: {data['agent_rank']}")
        raise HTTPException(status_code=400, detail=f"{data['agent_rank']} Illegal rank")
    logger.info(f"Agent created")
    return data

@router.get("")
def get_all_agents():
    return dbagant.get_all_agents()

@router.get("/{id}")
def agent_by_id(id: int):
    agent = dbagant.get_agent_by_id(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{id}")
def update_agent(id: int, agent: UpdateAgent):
    logger.info(f"Updating agent {id}")
    updated = dbagant.update_agent(id, agent.model_dump(exclude_unset=True, exclude_none= True))
    if updated is None:
        logger.warning(f"Agent {id} not found while updating")
        raise HTTPException(status_code=404, detail="Agent not found")
    if updated is False:
        logger.warning(f"No valid {id}")
        raise HTTPException(status_code=400, detail="Insert valid fields")
    return updated

@router.put("/{id}/deactivate")
def deactivate(id: int):
    logger.info(f"Deactivating agent {id}")
    deactivated = dbagant.deactivate_agent(id)
    if not deactivated:
        logger.warning(f"Agent {id} not found while deactivating")
        raise HTTPException(status_code=404, detail="Agent not found")
    logger.info(f"Agent {id} deactivated")
    return {"message": "Agent deactivated"}


@router.get("/{id}/performance")
def agent_performance(id: int):
    performance = dbagant.get_agent_performance(id)
    if performance is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return performance
