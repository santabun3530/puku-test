from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RatingBase(BaseModel):
    rating: int
    comment: str

class RatingCreate(RatingBase):
    recipe_id: int

class RatingUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

class RatingResponse(RatingBase):
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime

    class Config:
        from_attributes = True