import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from .base import BaseModel


class ClothesSize(enum.Enum):
    XXS = 1
    XS = 2
    S = 3
    M = 4
    L = 5
    XL = 6
    XXL = 7

    def __str__(self):
        return self.name

class Item(BaseModel):
    __tablename__ = 'items'

    name = Column(String, nullable=False)
    clothe_size = Column(Enum(ClothesSize), nullable=True)
    shoes_size = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    picture = Column(LargeBinary())
    price = Column(Integer, nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")
