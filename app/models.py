from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str
    price: float


class ItemCreate(BaseModel):
    #fix name must be at least 3 char
    name: str = Field(min_length=3)
    price: float


class ItemUpdate(BaseModel):
    #fix:name must be at least 3 char
    name: Optional[str] = Field(min_length=3)
    price: Optional[float] = None
