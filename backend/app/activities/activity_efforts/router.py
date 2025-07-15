from typing import Annotated, Callable, Optional
from datetime import datetime

from activities.activity_efforts import schema as activity_efforts_schema
from activities.activity_efforts import crud as activity_efforts_crud
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
import session.security as session_security
import core.database as core_database

router = APIRouter()

@router.get("/activities/efforts", response_model=list[activity_efforts_schema.RelativeEffort] | None)
async def get_relative_efforts(
    db: Annotated[Session, Depends(core_database.get_db)],
    user_id: Annotated[int, Depends(session_security.get_user_id_from_access_token)],
    activity_type: int,
    date: Optional[str] = datetime.now().strftime("%Y-%m-%d"),
    interval: str = "monthly",
):
    return activity_efforts_crud.get_efforts(
        db=db,
        user_id=user_id,
        activity_type=activity_type,    
        date=date,
        interval=interval
    )