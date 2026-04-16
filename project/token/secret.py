from fastapi.security import HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

load_dotenv()

# Строковые переменные из .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
DATABASE_URL = os.getenv("DATABASE_URL")

# Объекты, создаваемые в коде (не из .env)
security = HTTPBearer()
pwd_context = PasswordHash.recommended()
engine = create_engine(DATABASE_URL, echo=False)