from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db_worker import DBSession
from db.models.base import BaseModel
from db.models.user import User

engine = create_engine('sqlite:///test.db', echo=True)

BaseModel.create_base(engine)

db = DBSession(sessionmaker(bind=engine)())

user_12 = User()
user_12.tg_id = 12
db.add_model(user_12)

db.commit_session()

db.close_session()