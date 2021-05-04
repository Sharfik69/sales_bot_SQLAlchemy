from sqlalchemy import Column, Integer, String, Enum, ForeignKey
import enum

from .base import BaseModel
from .category import Category

class ClothesSize(enum.Enum):
    XXS = 1
    XS = 2
    S = 3
    M = 4
    L = 5
    XL = 6
    XXL = 7


class Item(BaseModel):
    __tablename__ = 'items'

    name = Column(String, nullable=False)
    clothe_size = Column(Enum(ClothesSize), nullable=True)
    shoes_size = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))


