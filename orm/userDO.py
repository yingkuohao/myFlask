# encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# 把数据库表信息和python类关联起来
# create_engine返回一个engine实例,会根据数据库配置调用对应的DB api  ,注意python3的mysql是pymysql,不支持mysqld
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/blogs", echo=True)

Base = declarative_base()  # 定义基类,参加ORM映射的类要继承这个子类

class User(Base):
    __tablename__ = 'user'  # talbename

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(20))
    password = Column(String(20))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

