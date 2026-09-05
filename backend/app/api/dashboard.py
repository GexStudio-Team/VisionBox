from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.inventory import Item, ItemEvent, ItemStatus
from app.schemas.inventory import DashboardResponse

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse, tags=["Dashboard"])
def get_dashboard(db: Session = Depends(get_db)):
    total_items = db.scalar(select(func.count()).select_from(Item)) or 0
    active_items = (
        db.scalar(select(func.count()).select_from(Item).where(Item.status == ItemStatus.ACTIVE.value)) or 0
    )
    archived_items = total_items - active_items
    total_units = (
        db.scalar(select(func.coalesce(func.sum(Item.quantity), 0)).where(Item.status == ItemStatus.ACTIVE.value))
        or 0
    )
    recent_events = db.scalars(select(ItemEvent).order_by(ItemEvent.created_at.desc()).limit(8)).all()
    return DashboardResponse(
        total_items=total_items,
        active_items=active_items,
        archived_items=archived_items,
        total_units=total_units,
        recent_events=recent_events,
    )
