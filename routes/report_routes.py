from fastapi import APIRouter, HTTPException

from database.mission_db import dbmission
from database.agent_db import dbagant

router = APIRouter(prefix="/reports")


@router.get("/summary")
def general_report():
    return {
        "active_agents_count": dbagant.count_active_agents(),
        "total_missions": dbmission.count_all_missions(),
        "open_missions": dbmission.count_open_missions(),
        "completed_missions": dbmission.count_by_status("Completed"),
        "failed_missions": dbmission.count_by_status("Failed"),
        "critical_missions": dbmission.count_critical_missions(),
    }



@router.get("/missions-by-status")
def mission_by_status():
    return {
        "open": dbmission.count_by_status("New") + dbmission.count_by_status("Assigned"),
        "in_progress": dbmission.count_by_status("In Progress"),
        "completed": dbmission.count_by_status("Completed"),
        "failed": dbmission.count_by_status("Failed"),
        "canceled": dbmission.count_by_status("Cancelled"),
    }





@router.get("/top-agent")
def grt_top_agent():
    top_agent = dbmission.get_top_agent()
    if top_agent is None:
        raise HTTPException(status_code=404, detail="No agents found")
    return top_agent
