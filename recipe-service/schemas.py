from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: str
    instructions: str
    cooking_time: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
    cooking_time: Optional[int] = None

class RecipeResponse(RecipeBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True