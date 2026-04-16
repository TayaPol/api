from project.dbforapi import s, Message, Post
from datetime import datetime
from project.log_config import logger


def get_last_message(limit: int = 50):
    return s.query(Message).order_by(Message.time_send.asc()).limit(limit).all()

# функция для просмотра всех постов
def get_post():
    return s.query(Post.user_id, Post.post_content, Post.time_post).all()

# функция для сохранения постов
def save_post(user_id: int, post_content: str):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post = Post(user_id=user_id, post_content=post_content, time_post=now_str)
    s.add(post)
    s.commit()
    logger.info(f"Пользователь {user_id} успешно опубликовал пост")
    return post

def save_message(sender_email: str, content: str):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = Message(sender_email=sender_email, content=content, time_send=now_str)
    logger.info(f"Сообщение {content} от {sender_email} успешно сохраненно в БД")
    s.add(msg)
    s.commit()
    return msg