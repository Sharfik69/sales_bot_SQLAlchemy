from telebot import types

def remove_keyboard():
    return types.ReplyKeyboardRemove()

def main_menu():
    markup = types.ReplyKeyboardMarkup(True, True)

    catalog = types.KeyboardButton('Каталог📄')
    shop_bucket = types.KeyboardButton('Корзина 🛍')
    sett = types.KeyboardButton('Настройки⚙️')

    markup.add(catalog, shop_bucket, sett)

    return markup
