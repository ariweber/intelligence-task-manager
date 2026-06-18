from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import servis

from database.mission_db import dbmission

class CreateMission(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1, max_length=50)
    difficulty: int = Field(..., ge=1, le=10)
    importance: int = Field(..., ge=1, le=10)

Status = Literal['New', 'Assigned', 'In Progress', 'Completed', 'Failed', 'Cancelled']
class UpdateStatus(BaseModel):
    status: Status


router = APIRouter(prefix="/missions")


@router.post("", status_code=201)
def create_mission(mission: CreateMission):
    data = mission.model_dump()
    data["status"] = "New"
    data["risk_level"] = servis.check_risk_level(data["difficulty"], data["importance"])
    return dbmission.create_mission(data)


@router.get("")
def get_all_missions():
    return dbmission.get_all_missions()



@router.get("/{id}")
def missions_by_id(id: int):
    mission = dbmission.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    return mission

@router.put("/{id}/assign/{agent_id}")
def assign(id: int, agent_id: int):
    return servis.assign(id, agent_id)
    



@router.put("/{id}/start")
def status_update_start(id: int):
    return servis.change_status(id, "Assigned", "In Progress")

@router.put("/{id}/complete")
def status_update_complete(id: int):
    return servis.change_status(id, "In Progress", "Completed")


@router.put("/{id}/fail")
def status_update_fail(id: int):
    return servis.change_status(id, "In Progress", "Failed")

@router.put("/{id}/cancel")
def status_update_cancel(id:int):
    return servis.change_status(id, "Assigned", "Cancelled")

