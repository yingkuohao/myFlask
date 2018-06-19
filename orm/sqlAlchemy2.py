# encoding=utf-8

from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from userDO import User, Base, engine

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/blogs", echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

# 1. 简单查询
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)

for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

# 可以重命名
from sqlalchemy.orm import aliased

user_alias = aliased(User, name='user_alias')

# 返回元组
for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias)

# offset limit
for u in session.query(User).order_by(User.id)[1:3]:
    print("limit:", u)

# 2.筛选操作
for name, in session.query(User.name).filter_by(fullname='Ed Jones'):  # filter_by后边跟随一个k-v
    print("filter_by=", name)  # name后边不加逗号是一个tuple,加上逗号代表拆分

for name, in session.query(User.name).filter(User.fullname == 'Ed Jones'):  # filter后跟随一个boolean表达式
    print("filter=", name)

for name, in session.query(User.name).filter(User.fullname.like('%Ed%')):  # like
    print("filter-like=", name)

for name, in session.query(User.name).filter(User.fullname.in_(['ed', 'wendy', 'jack'])):  # in
    print("filter-in=", name)

for name, in session.query(User.name).filter(~User.fullname.in_(['ed', 'wendy', 'jack'])):  # not in
    print("filter-not in=", name)

for name, in session.query(User.name).filter(User.fullname == None):  # is null 或者:User.fullname.is_(None)
    print("filter-is null=", name)

for name, in session.query(User.name).filter(User.fullname != None):  # is not null 或者:User.fullname.isnot(None)
    print("filter-is not null=", name)

for name, in session.query(User.name).filter(User.fullname == 'Ed Jones',
                                             User.name == 'ed'):  # and
    print("filter-and=", name)

for name, in session.query(User.name).filter(or_(User.fullname == 'Ed Jones',
                                                 User.name == 'ed')):  # or
    print("filter-and=", name)

# for name, in session.query(User.name).filter(User.fullname.match('wendy')):  # like
#     print("filter-match=", name)

# 3.返回列表list和单项(Scalar)

query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
userList = query.all();
print("list=", userList)

firstItem = query.first();
print("firstItem=", firstItem)

# oneItem = query.one();            #当结果的数量不足一个或多余一个时会报错 ,sacalar()与one()类似,单返回的是单项而不是tuple
# print("oneItem=",oneItem)


# 4. 嵌入sql

from sqlalchemy import text

# 通过text()嵌入sql
for user in session.query(User).filter(text("id<224")).order_by(text('id')).all():
    print("text:", user.name)

query_with_params = session.query(User).filter(text("id<:value and name=:name")). \
    params(value=224, name='ed').order_by(User.id);
print("sql_with_parms=", query_with_params.first())
