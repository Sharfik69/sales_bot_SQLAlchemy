from telebot import types

from db.models.category import Category
from db.models.item import Item
from keyboards import remove_keyboard
import db.queries.user_queries as queries


class Admin:
    def __init__(self, bot, db):
        self.db = db
        self.bot = bot

    def add_category(self, message):
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.row('Отмена')

        self.bot.send_message(message.from_user.id, 'ДОБАВИТЬ КАТЕГОРИЮ.\nВведите имя новой категории товаров',
                              reply_markup=markup)

        def add_category2(message):
            new_category = message.text
            if new_category == 'Отмена':
                self.bot.send_message(message.from_user.id, 'Операция добавления отменена',
                                      reply_markup=remove_keyboard())
                return
            try:
                self.db.add_model(Category(category_name=new_category))
                self.db.commit_session()
                self.bot.send_message(message.from_user.id, 'Категория "{}" была добавлена'.format(new_category),
                                      reply_markup=remove_keyboard())
            except Exception as e:
                print(e)
                self.bot.send_message(message.from_user.id, 'Произошла ошибка',
                                      reply_markup=remove_keyboard())

        self.bot.register_next_step_handler(message, add_category2)


    def add_item(self, message):
        markup = types.ReplyKeyboardMarkup(True, True)
        all_category = queries.get_cagegories(self.db)
        for cat in all_category:
            markup.add(cat.category_name)

        markup.row('Отмена')
        self.bot.send_message(message.from_user.id, 'Выберете категорию, куда ходите добавить товар',
                              reply_markup=markup)

        def add_item_set_name(message):
            cat_name = message.text
            if cat_name == 'Отмена':
                return
            category = queries.get_category(self.db, cat_name)

            self.bot.send_message(message.from_user.id, 'Введите на каждой строке информацию о товаре. На первой '
                                                        'строке название товара \nцена \nразмер \nописание товара '
                                                        '\nа так же прикрепите фотографию',
                                  reply_markup=remove_keyboard())

            def add_item_final(message):
                photo = None
                about = None
                if message.photo is None:
                    about = message.text.split('\n')
                else:
                    raw = message.photo[-1].file_id
                    file_info = self.bot.get_file(raw)
                    photo = self.bot.download_file(file_info.file_path)
                    about = message.caption.split('\n')

                if len(about) != 4:
                    return
                print(photo)
                print(about)

                try:
                    item = Item(name=about[0], clothe_size=about[2], description=about[3],
                                category=category,
                                price=about[1],
                                picture=photo)
                    self.db.add_model(item)
                    self.db.commit_session()
                    self.bot.send_message(message.from_user.id, 'Товар добавлен')
                except Exception as e:
                    self.bot.send_message(message.from_user.id, 'Не удалось добавить товар')


            self.bot.register_next_step_handler(message, add_item_final)


        self.bot.register_next_step_handler(message, add_item_set_name)
