from db.db_worker import DBSession
from db.models.item import Item
from db.models.user import User
from db.models.category import Category


def check_user_in_db(session: DBSession, user_id: int):
    result = session.query(User).filter(User.tg_id == user_id).scalar()

    return result


def get_category(session: DBSession, cat_name: str):
    category = session.query(Category).filter(Category.category_name == cat_name).scalar()
    return category


def get_category_by_id(session: DBSession, cat_id: int):
    category = session.query(Category).filter(Category.id == cat_id).scalar()
    return category


def get_items_by_cat_id(session: DBSession, cat_id: int):
    items = session.query(Item).filter(Item.category_id == cat_id).all()
    return items


def get_cagegories(session: DBSession):
    result = session.query(Category).all()
    return result


def get_count_items(session: DBSession, user_id: int, item_id: int):
    pass


def get_items_by_object(session: DBSession):
    pass
