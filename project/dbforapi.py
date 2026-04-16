from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from project.token.secret import engine

Base = declarative_base()


class Person(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user")


# публикация постов
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    post_content = Column(String, nullable=False)
    time_post = Column(String, nullable=False)



# таблица для хранения сообщений
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True) # айди сообщения
    sender_email = Column(String, nullable = False) # почта отправителя
    content = Column(String, nullable = False) # текст сообщения
    time_send = Column(String, nullable = False) # время отправки соо



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()



