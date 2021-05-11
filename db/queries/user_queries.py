from db.db_worker import DBSession
from db.models.user import User
from db.models.category import Category


def check_user_in_db(session: DBSession, user_id: int):
    result = session.query(User).filter(User.tg_id == user_id).scalar()

    return result


def get_cagegories(session: DBSession):
    result = session.query(Category).all()
    return result


def get_items_by_object(session: DBSession):
    pass