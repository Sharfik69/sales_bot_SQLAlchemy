from telebot import types

from db.models.category import Category


class Admin:
    def __init__(self, bot, db):
        self.db = db
        self.bot = bot
        pass

    def add_category(self, message):
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.row('Отмена')

        self.bot.send_message(message.from_user.id, 'ДОБАВИТЬ КАТЕГОРИЮ.\nВведите имя новой категории товаров',
                              reply_markup=markup)

        def add_category2(message):
            new_category = message.text
            if new_category == 'Отмена':
                self.bot.send_message(message.from_user.id, 'Операция добавления отменена',
                                      reply_markup=types.ReplyKeyboardRemove())
                return
            try:
                self.db.add_model(Category(category_name=new_category))
                self.db.commit_session()
                self.bot.send_message(message.from_user.id, 'Категория "{}" была добавлена'.format(new_category),
                                      reply_markup=types.ReplyKeyboardRemove())
            except Exception:
                self.bot.send_message(message.from_user.id, 'Произошла ошибка',
                                      reply_markup=types.ReplyKeyboardRemove())

        self.bot.register_next_step_handler(message, add_category2)
