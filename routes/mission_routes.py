from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field
from typing import Optional, Literal
from database.mission_db import dbmission

router = APIRouter(prefix="/missions")



