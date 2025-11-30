# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# class Recipe(Base):
#     __tablename__ = "recipes"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), nullable=False)
#     description = Column(Text, nullable=False)
#     ingredients = Column(Text, nullable=False)
#     instructions = Column(Text, nullable=False)
#     cooking_time = Column(Integer, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # reference User
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # optional: link to Rating
#     ratings = relationship("Rating", back_populates="recipe", cascade="all, delete-orphan")

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from datetime import datetime

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # Match init.sql length
    description = Column(Text)
    ingredients = Column(Text)
    instructions = Column(Text)
    cooking_time = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_id = Column(Integer, nullable=False)  # Make sure this exists
