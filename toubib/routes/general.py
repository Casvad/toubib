from fastapi import APIRouter
from structlog import get_logger


log = get_logger()
router = APIRouter(tags=["General"])

@router.get("/health")
def health():
    "Return OK if app is reachable"
    return "OK"