# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from datetime import datetime

# Base = declarative_base()

# class Rating(Base):
#     __tablename__ = "ratings"
    
#     id = Column(Integer, primary_key=True, index=True)
#     rating = Column(Integer)
#     comment = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     recipe_id = Column(Integer, ForeignKey("recipes.id"))
    
#     user = relationship("User", back_populates="ratings")
#     recipe = relationship("Recipe", back_populates="ratings")

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    # user_id = Column(Integer, ForeignKey("users.id"))
    # recipe_id = Column(Integer, ForeignKey("recipes.id"))
    user_id = Column(Integer, nullable=False)    # Make sure this exists
    recipe_id = Column(Integer, nullable=False)  # Make sure this exists