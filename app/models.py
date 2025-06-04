from typing import Optional

from pydantic import BaseModel, Field

class Item(BaseModel):
    id: int
    name: str = Field(..., min_length=3)
    price: float = Field(..., ge=0)


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., ge=0)


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)
    price: Optional[float] = Field(default=None, ge=0)
