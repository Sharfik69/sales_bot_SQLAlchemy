from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)

base = declarative_base()


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return '<User(name="{}", fullname="{}")'.format(self.name, self.fullname)


base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

user_ivan = User(name='ivan', fullname='Ivan Ivanov')

session.add(user_ivan)
session.commit()

q = session.query(User).filter_by(name='ivan')

other_ivan = q.first()

print(other_ivan)

session.add_all([User(name='petr', fullname='Petr Petrov')])

session.commit()

user_ivan.fullname = 'Ivan Sidorov'

session.commit()

s = session.execute('select * from users')

records = s.first()
print(records)