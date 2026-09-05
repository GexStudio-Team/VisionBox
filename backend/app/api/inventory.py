from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.inventory import Item, ItemEvent, ItemStatus
from app.schemas.inventory import ItemCreate, ItemEventResponse, ItemResponse, ItemUpdate

router = APIRouter()

@router.get(
    "/inventory",
    response_model=list[ItemResponse],
    tags=["Inventory"],
    summary="Inventory",
    description="Returns the current inventory."
)

def get_inventory(
    search: str | None = None,
    category: str | None = None,
    item_status: ItemStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query: Select[tuple[Item]] = select(Item).order_by(Item.updated_at.desc())
    if search:
        query = query.where(Item.name.ilike(f"%{search.strip()}%"))
    if category:
        query = query.where(Item.category == category)
    if item_status:
        query = query.where(Item.status == item_status.value)
    return db.scalars(query.offset(offset).limit(limit)).all()


@router.post(
    "/inventory",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Inventory"],
    summary="Create inventory item",
)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**payload.model_dump())
    db.add(item)
    db.flush()
    db.add(ItemEvent(item_id=item.id, action="created", detail="Item created manually"))
    db.commit()
    db.refresh(item)
    return item


@router.get(
    "/inventory/{item_id}",
    response_model=ItemResponse,
    tags=["Inventory"],
    summary="Get inventory item",
)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return _get_item_or_404(item_id, db)


@router.patch(
    "/inventory/{item_id}",
    response_model=ItemResponse,
    tags=["Inventory"],
    summary="Update inventory item",
)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = _get_item_or_404(item_id, db)
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if isinstance(value, ItemStatus):
            value = value.value
        setattr(item, field, value)
    db.add(ItemEvent(item_id=item.id, action="updated", detail="Item fields updated"))
    db.commit()
    db.refresh(item)
    return item


@router.post(
    "/inventory/{item_id}/archive",
    response_model=ItemResponse,
    tags=["Inventory"],
    summary="Archive inventory item",
)
def archive_item(item_id: int, db: Session = Depends(get_db)):
    item = _get_item_or_404(item_id, db)
    item.status = ItemStatus.ARCHIVED.value
    db.add(ItemEvent(item_id=item.id, action="archived", detail="Item archived"))
    db.commit()
    db.refresh(item)
    return item


@router.get(
    "/inventory/{item_id}/events",
    response_model=list[ItemEventResponse],
    tags=["Inventory"],
    summary="List item history",
)
def get_item_events(item_id: int, db: Session = Depends(get_db)):
    _get_item_or_404(item_id, db)
    return db.scalars(
        select(ItemEvent).where(ItemEvent.item_id == item_id).order_by(ItemEvent.created_at.desc())
    ).all()


def _get_item_or_404(item_id: int, db: Session) -> Item:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item
