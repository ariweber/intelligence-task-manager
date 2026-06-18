from fastapi import APIRouter

router = APIRouter(prefix="/reports")


@router.get("summary/reports")
def general_report():
    pass

@router.get("missions-by-status")
def mission_by_status(status):
    pass


