from random import random

import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import types

import db.queries.user_queries as queries
import keyboards
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

address = 'Не указано'

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    print(user_id)
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
    elif command == 'Настройки⚙️':
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add('Отмена')
        bot.send_message(message.from_user.id, 'Ваш текущий адрес доставки и способ связи:\n{}'.format(address))
        bot.send_message(message.from_user.id, 'Введите новую контактную информацию или нажмите "отмена"', reply_markup=markup)
        bot.register_next_step_handler(message, new_addres)
    elif command == 'Корзина 🛍':
        markup = types.ReplyKeyboardMarkup(True, True)
        user = queries.get_user(db, message.from_user.id)
        items = user.items
        if len(items) > 0:
            summ = send_items_to_user(items, message, fo=True)
            markup.add('Оплатить')
            markup.add('Назад')
            bot.send_message(message.from_user.id, 'Ваша корзина вышла на {} рублей'.format(summ), reply_markup=markup)
            bot.register_next_step_handler(message, buy_bucket, summ)
        else:
            bot.send_message(message.from_user.id, 'Ваша корзина пуста')
            menu(message)


def buy_bucket(message, summ):
    t = message.text

    if t == 'Назад':
        menu(message)
    elif t == 'Оплатить':
        oplata = """
        Доброго времени суток, ваш номер заказа:  {}
Вам нужно оплатить следующую сумму:   {}
Оплата производится на карту Сбербанка:
0000 0000 0000 0001
❗️Внимание, у вас есть 30 минут на оплату, в противном случае, ваш заказ будет отменён❗️
""".format(int(random() * 10000), summ)
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.add("Я оплатил")
        markup.add("Я передумал")
        bot.send_message(message.from_user.id, oplata, reply_markup=markup)
        bot.register_next_step_handler(message, buy_bucket_final)


def buy_bucket_final(message):
    t = message.text

    if t == 'Я оплатил':
        bot.send_message(message.from_user.id, 'Ожидайте, с вами скоро свяжутся')
        menu(message)
    elif t == 'Я передумал':
        menu(message)


def new_addres(message):
    global address
    if message.text == 'Отмена':
        bot.send_message(message.from_user.id, 'Отменено', keyboards.remove_keyboard())
        menu(message)
    else:
        address = message.text
        bot.send_message(message.from_user.id, 'Контактная информация изменена', keyboards.remove_keyboard())
        menu(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('catalog'))
def show_objects_from_catalog(call):
    response = call.data.split()
    items = queries.get_items_by_cat_id(db, int(response[1]))
    send_items_to_user(items, call)
    print(response)


def send_items_to_user(items, call, fo=False):
    summ = 0
    for item in items:
        markup = types.InlineKeyboardMarkup(row_width=3)
        cnt = queries.get_count_items(db, queries.get_user(db, call.from_user.id), item.id)
        x = 'buck minus {}'.format(item.id)
        if fo:
            x = 'buck delete {}'.format(item.id)
        markup.add(types.InlineKeyboardButton('-', callback_data=x),
                   types.InlineKeyboardButton(str(cnt), callback_data='pass'),
                   types.InlineKeyboardButton('+', callback_data='buck plus {}'.format(item.id)))
        name = item.name
        about = item.description
        price = item.price
        summ += price * cnt
        size = item.clothe_size
        photo = item.picture
        message_item = """
            Товар: {}
Цена: {}
Размер: {}
О товаре: {}
        """.format(name, price, str(size), about)
        bot.send_photo(call.from_user.id, photo=photo, caption=message_item, reply_markup=markup)
    return summ

@bot.callback_query_handler(func=lambda call: call.data.startswith('buck'))
def add_or_pop_item(call):
    response = call.data.split()
    user = queries.get_user(db, call.from_user.id)
    item = queries.get_item_by_id(db, int(response[2]))
    if response[1] == 'plus':
        user.items.append(item)
        db.commit_session()

        markup = types.InlineKeyboardMarkup(row_width=3)
        cnt = queries.get_count_items(db, queries.get_user(db, call.from_user.id), item.id)

        markup.add(types.InlineKeyboardButton('-', callback_data='buck delete {}'.format(item.id)),
                   types.InlineKeyboardButton(str(cnt), callback_data='{}'.format(random())),
                   types.InlineKeyboardButton('+', callback_data='buck plus {}'.format(item.id)))
        print(cnt)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif response[1] == 'delete':
        user.items.remove(item)
        db.commit_session()

        markup = types.InlineKeyboardMarkup(row_width=3)
        cnt = queries.get_count_items(db, queries.get_user(db, call.from_user.id), item.id)
        markup.add(types.InlineKeyboardButton('-', callback_data='buck delete {}'.format(item.id)),
                   types.InlineKeyboardButton(str(cnt), callback_data='{}'.format(random())),
                   types.InlineKeyboardButton('+', callback_data='buck plus {}'.format(item.id)))

        if cnt == 0:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=markup)


bot.polling()
