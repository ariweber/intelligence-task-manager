def check_risk_level(difficulty:int,importance:int):
    result = (difficulty * 2) + importance
    risk_level = ""
    if result <= 9:
        risk_level = "low"
    elif 9 < risk_level < 18:
        risk_level = "medium"
    elif 17 < risk_level < 25:
        risk_level = "hige"
    elif risk_level > 25:
        risk_level = "critical"
    return risk_level


def ceeck_ransition_status(current, new_status):
    approval = False
    if current == "New" and new_status in ("Assigned", "Cancelled"):
       approval = True
    if current == "Assigned" and new_status in ("In Progress", "Cancelled"):
        approval = True
    if current == "In Progress" and new_status in ("Completed", "Failed", "Cancelled"):
        approval = True
    return approval
