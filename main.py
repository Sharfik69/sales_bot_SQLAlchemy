import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db.queries.user_queries as queries
import settings
from admin_tools import Admin
from db.db_worker import DBSession
from db.models.base import BaseModel
from db.models.user import User

engine = create_engine('sqlite:///test.db', echo=True)

BaseModel.create_base(engine)

db = DBSession(sessionmaker(bind=engine)())

bot = telebot.TeleBot(settings.__TELEGRAM_TOKEN__, parse_mode=None)

admin = Admin(db=db, bot=bot)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    response = queries.check_user_in_db(db, user_id)
    if response is None:
        db.add_model(User(tg_id=user_id))
        db.commit_session()
        bot.send_message(message.from_user.id, 'Добро пожаловать, вы успешно зарегестрировались')


@bot.message_handler(commands=['add_category'])
def command_add_category(message):
    user_id = message.from_user.id

    if user_id in settings.__ADMINS__:
        admin.add_category(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'cancel':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Отмена', reply_markup=None)


bot.polling()
