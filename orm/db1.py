# encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pymysql
from userDO import User, Base, engine

Base.metadata.create_all(engine)  # 创建上面定义的表

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print("ed_user", ed_user)

SessionCls = sessionmaker(bind=engine)  # 创建与数据库的会话session class,注意这里返回的是个class,不是实例
session = SessionCls()
session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()
print("ed_user", our_user)

our_user.password = '11234'

session.commit();
