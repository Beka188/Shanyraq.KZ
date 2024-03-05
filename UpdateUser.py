from typing import Optional

from pydantic import BaseModel


class UpdateUserInfo(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None


class UpdateAd(BaseModel):
    type: Optional[str] = None
    price: Optional[int] = None
    address: Optional[str] = None
    area: Optional[float] = None
    rooms_count: Optional[int] = None
    description: Optional[str] = None
