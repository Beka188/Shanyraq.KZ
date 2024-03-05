from typing import Optional

from pydantic import BaseModel


class UpdateUserInfo(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None
