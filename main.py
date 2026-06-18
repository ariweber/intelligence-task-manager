from database.db_connection import DB
from fastapi import FastAPI
import logging
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_routrs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()],)

logger = logging.getLogger(__name__)


DB.setup()

app = FastAPI()

app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_routrs)

logger.info("Application started and routers registered")











