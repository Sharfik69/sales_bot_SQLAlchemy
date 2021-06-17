from sqlalchemy import Column, Integer, Table, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from .base import BaseModel, Base

shopping_basket = Table('shopping_basket', Base.metadata,
                        Column('id', Integer, primary_key=True, nullable=False),
                        Column('user_id', Integer, ForeignKey('users.id')),
                        Column('item_id', Integer, ForeignKey('items.id')),
                        )


class User(BaseModel):
    __tablename__ = 'users'

    tg_id = Column(Integer, nullable=False)


    items = relationship("Item",
                         secondary=shopping_basket, backref='user_backref')
