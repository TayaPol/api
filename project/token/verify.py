from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import jwt
from project.token.secret import SECRET_KEY, ALGORITHM, security
from project.log_config import logger




# проверяет действительность токена
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])  # расшифровывает токен
        user_id: int = payload.get("sub")
        user_email: str = payload.get("email")
        user_role: str = payload.get("role")
        if user_id is None or user_email is None or user_role is None:
            # обработка ошибок
            logger.warning(f"У пользователя {user_email} недействительный токен")
            raise HTTPException(status_code=401, detail="Недействительный токен")
        return user_id, user_email, user_role
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Недействительный токен")


def admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id, user_email, user_role = verify_token(credentials)
    if user_role != "admin":
        logger.warning(f"Пользователю {user_email} отказано в доступе")
        raise HTTPException(status_code = 403, detail = "У вас нет прав")
    logger.info(f"Пользователь {user_email} вошел как админ")
    return user_id, user_email, user_role