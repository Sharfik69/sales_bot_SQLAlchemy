from db.db_worker import DBSession
from db.models.user import User


def check_user_in_db(session: DBSession, user_id: int):
    result = session.query(User).filter(User.tg_id == user_id).scalar()

    return result
