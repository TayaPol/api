from fastapi import FastAPI
from fastapi.responses import FileResponse
from project.endpoints.admin import router as admin_router
from project.endpoints.auth import router as auth_router
from project.endpoints.auth_user import router as user_router
from project.endpoints.all_users import router as posts_router
from project.endpoints.socket import router as chat_router
from project.dbforapi import Base, engine
from project.log_config import logger
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при запуске
    logger.info("Приложение запущено")
    yield
    # Действия при остановке (опционально)
    logger.info("Приложение завершает работу")


app = FastAPI(lifespan=lifespan)

# Создание таблиц в базе данных (если ещё не созданы)
Base.metadata.create_all(bind=engine)

# Подключение всех роутеров
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)
app.include_router(chat_router)

# Эндпоинты для HTML-страниц (они лежат в папке templates)
@app.get("/")
def root():
    return FileResponse("templates/index.html")

@app.get("/look_post")
def look_post():
    return FileResponse("templates/index2.html")


@app.get("/chat")
def chat_page():
    return FileResponse("templates/index3.html")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)