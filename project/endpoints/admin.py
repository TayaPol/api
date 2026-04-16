from fastapi import APIRouter, Depends, HTTPException
from project.token.verify import admin
from project.log_config import logger
from project.dbforapi import s, Person, Post
from project.schemas import UR

router = APIRouter(prefix="/admin", tags=["Админка"])


# админский эндпоинт
@router.delete("/del_want_user", tags=["Админка"])
def del_user(data_del: int, current_user: tuple = Depends(admin)):
    user_id, user_email, user_role = current_user
    id_user_del = s.query(Person).filter(Person.user_id == data_del).first()
    if not id_user_del:
        raise HTTPException(status_code=404, detail = "Такого пользователя нет")
    s.delete(id_user_del)
    s.commit()
    logger.info(f"{user_role} {user_email} удалил {id_user_del.email}")
    return f"Вы {user_role} {user_email} удалили {id_user_del.email}"

# админский эндпоинт смена роли"
@router.post("/role_change", tags=["Админка"])
def change_role(data_user_id: int, data_role_new = UR ,current_user: tuple = Depends(admin)):
    user_id, user_email, user_role = current_user
    id_user_change = s.query(Person).filter(Person.user_id == data_user_id).first()
    if not id_user_change:
        raise HTTPException(status_code = 404, detail = "Такого пользователя нет")
    new = s.query(Person).filter(Person.email == id_user_change.email).update({"role": data_role_new})
    s.commit()
    logger.info(f"{user_email} сменил у {id_user_change.email} роль на {data_role_new}")
    return f"Вы {user_email} сменили у {id_user_change.email} роль на {data_role_new}"


# админский эндпоинт удаления постов
@router.delete("/post_user", tags=["Админка"])
def del_user_post(data_user_id_post = int, current_user: tuple = Depends(admin)):
    user_id, user_email, user_role = current_user
    want_del_post = s.query(Post).filter(Post.user_id == data_user_id_post).first()
    print(want_del_post)
    if not want_del_post:
        raise HTTPException(status_code = 404, detail = "Такого пользователя не существует")
    s.delete(want_del_post)
    s.commit()
    logger.info(f"{user_email} удалил у {want_del_post.user_id} пост {want_del_post.post_content}")
    return f"Вы {user_email} удалили у {want_del_post.user_id} пост {want_del_post.post_content}"