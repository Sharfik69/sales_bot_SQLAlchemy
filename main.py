import telebot
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

import settings
from db.db_worker import DBSession
from db.models.base import BaseModel
from db.models.user import User

engine = create_engine('sqlite:///test.db', echo=True)

BaseModel.create_base(engine)

db = DBSession(sessionmaker(bind=engine)())

bot = telebot.TeleBot(settings.__TELEGRAM_TOKEN__, parse_mode=None)


@bot.message_handler(commands=['add_users'])
def add_users(message):
    db.add_model(User(tg_id=1234))
    db.add_model(User(tg_id=1232))
    db.commit_session()
    bot.send_message(message.from_user.id, 'Добавили двух юзеров')


@bot.message_handler(commands=['check_users'])
def check_users(message):
    # s = db.session.execute('select * from users')
    s = db.session.query(func.count(User.id)).scalar()
    bot.send_message(message.from_user.id, str(s))


bot.polling()
# db.add_model(User(tg_id=123))
#
# db.commit_session()
#
# db.close_session()