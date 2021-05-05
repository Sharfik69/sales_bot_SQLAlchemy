from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'

    category_name = Column(String)