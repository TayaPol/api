from fastapi import APIRouter, Depends, HTTPException, Response
from project.token.secret import pwd_context, security
from project.token.create_token import create_access_token, create_refresh_token
from project.log_config import logger
import jwt
from project.token.secret import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPAuthorizationCredentials
from project.schemas import U
from project.dbforapi import s, Person




router = APIRouter(prefix="/auth", tags=["Вход в систему"])

# регистрация пользователя
@router.post("/auth", tags=["Вход в систему"])
def auth(data: U, response: Response):
    entrance_user = s.query(Person).filter(Person.email == data.email).first()
    if entrance_user:
        logger.warning(f"Пользователю отказано в регистрации")
        raise HTTPException(status_code = 400, detail="Такой пользователь уже существует")
    else:
        hashed_password = pwd_context.hash(data.password)
        users = Person(email=data.email, password=hashed_password)
        s.add(users)
        s.commit()
        token = create_access_token(data={"sub":users.user_id, "email": users.email, "role": users.role})
        token_r = create_refresh_token(data={"sub": users.user_id, "email": users.email, "role": users.role})
        return {"access_token": token, "refresh_token": token_r, "token_type": "bearer"}



# вход пользователя
@router.post("/entrance", tags=["Вход в систему"])
def entrance(data: U       , response: Response):
    entrance_user = s.query(Person).filter(Person.email == data.email).first()
    if not entrance_user:
        logger.warning(f"Пользователь не смог войти в аккаунт, тк почты нет в БД")
        raise HTTPException(status_code=401, detail="Такого пользователя не существует или почта введена неверно!")
    if not pwd_context.verify(data.password, entrance_user.password): # проверяет соответсвует ли пароль его хэшу
        logger.warning(f"Пользователь {entrance_user.email} не смог войти в аккаунт, пароль введен неверно")
        raise HTTPException(status_code=401, detail="Такого пользователя не существует или пароль введен неверно!")
    token = create_access_token(data={"sub": entrance_user.user_id, "email": entrance_user.email, "role": entrance_user.role}) # отдаем аксес токен
    token_r = create_refresh_token(data={"sub": entrance_user.user_id, "email": entrance_user.email, "role": entrance_user.role}) # отдаем рефреш токен
    response.set_cookie(key = "access_token", value=token)
    response.set_cookie(key = "refresh_token",  value=token_r)
    return {"access_token": token, "refresh_token": token_r, "token_type": "bearer"}




# создаем эндпоинт для обновления аксес токена с помощью рефреш токена
@router.post("/update_token", tags=["Вход в систему"])
def update_access_token(credentials: HTTPAuthorizationCredentials =Depends(security)):
    token_r = credentials.credentials
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
        raise HTTPException(status_code = 401, detail = "Токен недействительный")
    user_id: str = payload.get("sub")
    user_email: str = payload.get("email")
    user_for_db = s.query(Person).filter(Person.user_id == user_id).first()
    if user_for_db is None:
        raise HTTPException(status_code=401, detail = "Такого пользователя нет")
    else:
        new_access_token = create_access_token(data={"sub": str(user_id), "email": str(user_email), "role": user_for_db.role})
        logger.info(f"У пользователя {user_email} обновлены токены")
        return {"access_token": new_access_token, "refresh_token": token_r, "token_type": "bearer"}