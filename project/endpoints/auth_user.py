from fastapi import APIRouter, Depends, HTTPException
from project.token.verify import verify_token
from project.token.secret import pwd_context
from project.log_config import logger
from project.schemas import PostPost, U, UNP, UN
from project.CRUD import save_post
from project.dbforapi import s, Person, Post



router = APIRouter(prefix="/users", tags=["Пользователь"])


@router.post("/post", tags=["Пользователь"])
def post_send(data_post: PostPost, current_user: tuple = Depends(verify_token)):
    try:
        user_id, user_email, user_role = current_user
    except ValueError:
        raise HTTPException(status_code=401, detail="Ошибка публикации")
    save_post(user_id=user_id, post_content=data_post.content)
    logger.info(f"Пользователь {user_email} успешно опубликовал пост")
    return {f"Пост опубликован, {user_email}!"}



# для просмотра инфы о себе
@router.get("/my_info", tags=["Пользователь"])
def get_my_info(current_user: tuple = Depends(verify_token)):
    user_id, user_email, user_role = current_user
    posts = s.query(Post.id, Post.post_content).filter(Post.user_id == user_id).all()
    logger.info(f"Пользователь {user_email} успешно получил информацию о себе")
    return f"Информация о вас: Ваш айди: {user_id} Ваша почта: {user_email} Ваши посты: {posts}"



# удалить свой пост
@router.delete("/del_post", tags=["Пользователь"])
def del_my_post(data_id = int, current_user: tuple = Depends(verify_token)):
    user_id, user_email, user_role = current_user
    id_post = s.query(Post).filter(Post.id == data_id).first()
    if not id_post:
        raise HTTPException(status_code=404, detail="Элемент не существует")
    s.delete(id_post)
    s.commit()
    posts = s.query(Post.post_content).filter(Post.user_id == user_id).all()
    logger.info(f"Пользователь {user_email} успешно удалил свой пост")
    return f"id удалённого поста: {data_id}; ваши посты: {posts}"



@router.patch("/update_email", tags=["Пользователь"])
def update_email(data_old: U, data_new: UN, current_user: tuple = Depends(verify_token)):
    user_id, user_email, user_role = current_user
    old = s.query(Person.email).filter(data_old.email == user_email).first()
    if not old:
        logger.warning(f"Пользователь {user_email} не смог сменить почту")
        raise HTTPException(status_code=404, detail="Старые данные введены неверно")
    # проверка пароля
    user = s.query(Person).filter(Person.email == data_old.email).first()
    if not pwd_context.verify(data_old.password, user.password):  # проверяет соответсвует ли пароль его хэшу
        logger.warning(f"Пользователь {user_email} не смог сменить почту")
        raise HTTPException(status_code=404, detail="Неверный пароль")
    if data_old.email == data_new.email:
        logger.warning(f"Пользователь {user_email} не смог сменить почту")
        return "Новая почта не должна совпадать со старой"
    try:
        new = s.query(Person).filter(Person.email == user_email).update({"email": data_new.email})
        s.commit()
        logger.info(f"Пользователь {user_email} сменил почту")
        return f"Вы сменили почту! Старая почта: {data_old.email}, новая почта: {data_new.email}"
    except:
        logger.warning(f"Пользователь {user_email} не смог сменить почту")
        return "Неверно введена почта"


@router.patch("/update_password", tags=["Пользователь"])
def update_password(data_old: U, data_new: UNP, current_user: tuple = Depends(verify_token)):
    user_id, user_email, user_role = current_user
    old = s.query(Person.email).filter(data_old.email == user_email).first()
    if not old:
        logger.warning(f"Пользователь {user_email} не смог сменить пароль")
        raise HTTPException(status_code=404, detail="Почта введена неверно")
    # проверка пароля
    user = s.query(Person).filter(Person.email == data_old.email).first()
    if not pwd_context.verify(data_old.password, user.password):  # проверяет соответсвует ли пароль его хэшу
        logger.warning(f"Пользователь {user_email} не смог сменить пароль")
        raise HTTPException(status_code=404, detail="Неверный пароль")
    hashed_password = pwd_context.hash(data_new.password)
    try:
        new = s.query(Person).filter(Person.user_id == user_id).update({"password": hashed_password})
        s.commit()
        logger.info(f"Пользователь {user_email} сменил пароль")
        return f"Вы успешно сменили пароль! Старый пароль: {data_old.password}, новый пароль: {data_new.password}"
    except:
        logger.warning(f"Пользователь {user_email} не смог сменить пароль")
        return "Попробуйте позже"