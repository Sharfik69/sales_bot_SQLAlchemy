from sqlalchemy import Column, String

from .base import BaseModel


class Category(BaseModel):
    __tablename__ = 'categories'

    category_name = Column(String)
