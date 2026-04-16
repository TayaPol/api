import jwt
import datetime
from typing import Optional
from project.token.secret import SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS
from project.log_config import logger




def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None): # expires_delta означает время действия токена
    logger.debug(f"Создание access токена {data}")
    to_encode = data.copy() # создаёт копию переданных данных
    if expires_delta:
        # устанавливается время истечения токена как сумма текущего времени и указанного параметра
        expire = datetime.datetime.now() + expires_delta
        logger.debug(f"Установлено время иcтечения через {expires_delta} {expire}")
    else:
        # устанавливается время истечения токена как сумма текущего времени и 15 минут
        expire = datetime.datetime.now() + datetime.timedelta(minutes=15)
        logger.debug(f"Установлено время иcтечения 15 минут")
    to_encode.update({"exp": expire}) # добавляет время истечения в копию переданных данных
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # кодирует данные с помощью секретного ключа и определённого алгоритма
    logger.info("Access токен успешно создан")
    return encoded_jwt # возвращает закодированный токен


def create_refresh_token(data: dict):
    logger.debug(f"Создание refresh токена {data}")
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS) # текущее время + указанный интервал
    logger.debug(f"Время токена выделено {expire}")
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("Refresh токен успешно создан")
    return encoded_jwt