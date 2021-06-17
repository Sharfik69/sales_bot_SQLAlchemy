from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db_worker import DBSession
from db.models.base import BaseModel
from db.models.category import Category
from db.models.item import Item
from db.models.user import User

engine = create_engine('sqlite:///test.db', echo=True)

BaseModel.create_base(engine)

db = DBSession(sessionmaker(bind=engine)())

user1 = User(tg_id=1)

db.add_model(user1)

category1 = Category(category_name='Hoodie')

db.add_model(category1)

item1 = Item(name='item1', clothe_size='XS', description='Крутой товар', category=category1, picture=None)
item2 = Item(name='item2', clothe_size='S', description='Крутой товар но размером больше', category=category1,
             picture=None)

db.add_model(item1)
db.add_model(item2)

user1.items.append(item1)
user1.items.append(item2)

db.commit_session()
db.close_session()
