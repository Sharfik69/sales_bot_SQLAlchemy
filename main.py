import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import types

import db.queries.user_queries as queries
import settings
from admin_tools import Admin
from db.db_worker import DBSession
from db.models.base import BaseModel
from db.models.user import User
from keyboards import main_menu

engine = create_engine('sqlite:///test.db?check_same_thread=False', echo=True)

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
        bot.send_message(message.from_user.id, 'Добро пожаловать, вы успешно зарегестрировались', reply_markup=main_menu())


@bot.message_handler(commands=['add_category'])
def command_add_category(message):
    user_id = message.from_user.id

    if user_id in settings.__ADMINS__:
        admin.add_category(message)

@bot.message_handler(commands=['add_item'])
def command_add_item(message):
    user_id = message.from_user.id

    if user_id in settings.__ADMINS__:
        admin.add_item(message)


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.from_user.id, 'Главное меню', reply_markup=main_menu())
    bot.register_next_step_handler(message, next_menu)


def next_menu(message):
    command = message.text
    if command == 'Каталог📄':
        all_category = queries.get_cagegories(db)
        markup = types.InlineKeyboardMarkup(row_width=2)
        for cat in all_category:
            key_ = types.InlineKeyboardButton(cat.category_name, callback_data='catalog {}'.format(cat.id))
            markup.add(key_)
            print(cat.category_name, cat.id)
        bot.send_message(message.from_user.id, 'Категории', reply_markup=markup)





@bot.callback_query_handler(func=lambda call: call.data.startswith('catalog'))
def show_objects_from_catalog(call):
    response = call.data.split()
    items = queries.get_items_by_cat_id(db, int(response[1]))
    for item in items:
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add( types.InlineKeyboardButton('-', callback_data='minus {}'.format(item.id)),
                    types.InlineKeyboardButton('0', callback_data='minus {}'.format(item.id)),
                    types.InlineKeyboardButton('+', callback_data='minus {}'.format(item.id)))
        name = item.name
        about = item.description
        price = item.price
        size = item.clothe_size
        photo = item.picture
        message_item = """
            Товар: {}
Цена: {}
Размер: {}
О товаре: {}
        """.format(name, price, str(size), about)
        bot.send_photo(call.from_user.id, photo=photo, caption=message_item, reply_markup=markup)
    print(response)



bot.polling()
