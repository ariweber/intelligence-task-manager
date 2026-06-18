import logging
from database.mission_db import dbmission
from database.agent_db import dbagant
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def check_risk_level(difficulty:int,importance:int):
    result = (difficulty * 2) + importance
    if result <= 9:
        risk_level = "Low"
    elif result <= 17:
        risk_level = "Medium"
    elif result <= 25:
        risk_level = "High"
    else:
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
    logger.info(f"Changing status of mission {id} from {current} to {new_status}")
    mission = dbmission.get_mission_by_id(id)
    if mission is None:
        logger.warning(f"Mission {id} not found while changing status")
        raise HTTPException(status_code=404, detail="mission not found")
    if mission["status"] != current:
        logger.warning(f"Mission {id} status mismatch: expected {current} but found {mission['status']}")
        raise HTTPException(status_code=400, detail="Invalid status")
    if not check_ransition_status(current, new_status):
        logger.warning(f"Invalid status transition for mission {id}: {current} -> {new_status}")
        raise HTTPException(status_code=400, detail=f"Cannot change status from {current} to {new_status}")

    dbmission.update_mission_status(id, new_status)
    if new_status == "Completed":
        logger.info(f"Mission {id} completed by agent {mission['assigned_agent_id']}")
        dbagant.increment_completed(mission["assigned_agent_id"])
    if new_status == "Failed":
        logger.info(f"Mission {id} failed by agent {mission['assigned_agent_id']}")
        dbagant.increment_failed(mission["assigned_agent_id"])
    logger.info(f"Mission {id} status changed to {new_status}")
    return dbmission.get_mission_by_id(id)


def assign(id, agent_id):
    logger.info(f"Attempting to assign mission {id} to agent {agent_id}")
    mission = dbmission.get_mission_by_id(id)
    if mission is None:
        logger.warning(f"Mission {id} not found while assigning")
        raise HTTPException(status_code=404, detail="mission not found")
    if mission["status"] != "New":
        logger.warning(f"Mission {id} cannot be assigned, current status is {mission['status']}")
        raise HTTPException(status_code=400, detail="Only a mission with status New can be assigned")

    agent = dbagant.get_agent_by_id(agent_id)
    if agent is None:
        logger.warning(f"Agent {agent_id} not found while assigning mission {id}")
        raise HTTPException(status_code=404, detail="agent not found")
    if not agent["is_active"]:
        logger.warning(f"Inactive agent {agent_id} cannot accept mission {id}")
        raise HTTPException(status_code=400, detail="Inactive agent cannot accept missions")

    open_missions = dbmission.get_open_missions_by_agent(agent_id)
    if len(open_missions) >= 3:
        logger.warning(f"Agent {agent_id} already has {len(open_missions)} open missions")
        raise HTTPException(status_code=400, detail="Agent already has 3 open missions")
    if mission["risk_level"] == "Critical" and agent["agent_rank"] != "Commander":
        logger.warning(f"Agent {agent_id} (rank {agent['agent_rank']}) cannot accept Critical mission {id}")
        raise HTTPException(status_code=400, detail="Only a Commander can accept a Critical mission")

    dbmission.assign_mission(id, agent_id)
    dbmission.update_mission_status(id, "Assigned")
    logger.info(f"Mission {id} successfully assigned to agent {agent_id}")
    return dbmission.get_mission_by_id(id)


    
    
    

