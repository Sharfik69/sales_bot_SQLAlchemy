from sqlalchemy import Column, Integer, String, Enum, ForeignKey, LargeBinary
import enum

from sqlalchemy.orm import relationship

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
    picture = Column(LargeBinary())

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")

