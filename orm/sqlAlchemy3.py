# encoding=utf-8

from sqlalchemy import create_engine, or_, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, relationship
from userDO import User, Base, engine

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/blogs", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

#
# meta = MetaData()
# meta.bind = engine
# exist_user = Table('user', meta, autoload=True)
# new_column = Column('addresss', String(20))
# exist_user.addColumn(new_column)
# setattr('user', 'addresses',Column(String(20)))
# Base.metadata.create_all(engine)
User.addresses = relationship("Address", back_populates="user", order_by=Address.id)

jack = User(name='jack', fullname='Jack Bean', password='giffddd')

jack.addresses = [
    Address(email_address='jack@google.com'),
    Address(email_address='j25@yahoo.com')
]

session.add(jack)
session.commit()
