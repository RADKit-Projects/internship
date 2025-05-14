from typing import Optional

from pydantic import BaseModel, Field

class Item(BaseModel):
    id: int
    name: str
    price: float

#TASK 3: Added minimum length verification to item creation 
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3)
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
