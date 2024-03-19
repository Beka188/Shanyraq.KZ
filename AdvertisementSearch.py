from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class AdvertisementSearch(BaseModel):
    limit: int = Query(10, ge=1, le=100)
    offset: int = Query(0, ge=0)
    type: Optional[str] = None
    rooms_count: Optional[int] = None
    price_from: Optional[int] = None
    price_until: Optional[int] = None

