from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.inventory import ItemStatus


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    category: str | None = Field(default=None, max_length=80)
    description: str | None = None
    quantity: int = Field(default=1, ge=0)
    location: str | None = Field(default=None, max_length=120)
    image_url: str | None = Field(default=None, max_length=500)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    category: str | None = Field(default=None, max_length=80)
    description: str | None = None
    quantity: int | None = Field(default=None, ge=0)
    location: str | None = Field(default=None, max_length=120)
    image_url: str | None = Field(default=None, max_length=500)
    status: ItemStatus | None = None


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: ItemStatus
    created_at: datetime
    updated_at: datetime


class ItemEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    action: str
    detail: str | None
    created_at: datetime


class DashboardResponse(BaseModel):
    total_items: int
    active_items: int
    archived_items: int
    total_units: int
    recent_events: list[ItemEventResponse]
