from logging import getLogger
from sqlalchemy.orm import Session

from db.models.base import BaseModel

log = getLogger()

class DBSession(object):

    session: Session

    def __init__(self, session: Session):
        self.session = session

    def add_model(self, model: BaseModel):
        self.session.add(model)

    def delete_model(self, model: BaseModel):
        if model is None:
            log.warning('{}: Model is None'.format(__name__))

        try:
            self.session.delete(model)
        except Exception as e:
            log.error('{} - {}'.format(__name__, e))

    def commit_session(self):
        self.session.commit()

    def close_session(self):
        self.session.close()