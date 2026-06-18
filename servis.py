from database.mission_db import dbmission
from database.agent_db import dbagant
from fastapi import HTTPException
def check_risk_level(difficulty:int,importance:int):
    result = (difficulty * 2) + importance
    risk_level = ""
    if result <= 9:
        risk_level = "Low"
    elif 9 < result < 18:
        risk_level = "Medium"
    elif 17 < result < 25:
        risk_level = "High"
    elif result > 25:
        risk_level = "Critical"
    return risk_level


def check_ransition_status(current, new_status):
    approval = False
    if current == "New" and new_status in ("Assigned", "Cancelled"):
       approval = True
    if current == "Assigned" and new_status in ("In Progress", "Cancelled"):
        approval = True
    if current == "In Progress" and new_status in ("Completed", "Failed", "Cancelled"):
        approval = True
    return approval


def change_status(id, current ,new_status):
    mission = dbmission.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    if mission["status"] != current:
        raise HTTPException(status_code=400, detail="Invalid status")
    if not check_ransition_status(current, new_status):
        raise HTTPException(status_code=400, detail=f"Cannot change status from {current} to {new_status}")
    
    dbmission.update_mission_status(id, new_status)
    if new_status == "Completed":
        dbagant.increment_completed(mission["assigned_agent_id"])
    if new_status == "Failed":
        dbagant.increment_failed(mission["assigned_agent_id"])
    return mission    


def assign(id, agent_id):
    mission = dbmission.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="mission not found")
    if mission["status"] != "New":
        raise HTTPException(status_code=400, detail="Only a mission with status New can be assigned")

    agent = dbagant.get_agent_by_id(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    if not agent["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive agent cannot accept missions")

    open_missions = dbmission.get_open_missions_by_agent(agent_id)
    if len(open_missions) >= 3:
        raise HTTPException(status_code=400, detail="Agent already has 3 open missions")
    if mission["risk_level"] == "Critical" and agent["agent_rank"] != "Commander":
        raise HTTPException(status_code=400, detail="Only a Commander can accept a Critical mission")

    dbmission.assign_mission(id, agent_id)
    dbmission.update_mission_status(id, "Assigned")
    return dbmission.get_mission_by_id(id)


    
    
    

