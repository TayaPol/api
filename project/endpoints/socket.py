from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import jwt
from project.token.secret import SECRET_KEY, ALGORITHM
from project.CRUD import save_message, get_last_message


router = APIRouter(tags=["Страница"])


class ConnectionManager:
    def __init__(self):
        # Список подключений
        self.active_connections: List[WebSocket] = []

    # добавляет новое WebSocket соединение в список active_connections
    async def connect(self, websocket: WebSocket):
        # Принимаем новое соединение и добавляем его в список активных
        await websocket.accept() # подтверждает вебсокет соединение между клиентом и сервером
        self.active_connections.append(websocket)

    # удаляет соединение, если клиент отключается
    def disconnect(self, websocket: WebSocket):
        # Убираем отключенного клиента из списка
        self.active_connections.remove(websocket)

    # рассылает сообщение всем активным соединениям
    async def broadcast(self, message: str):
        # Отправляем сообщение всем подключенным пользователям
        for connection in self.active_connections:
            await connection.send_text(message)

# Инициализация менеджера подключений
manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    token = websocket.headers.get("cookie").split("access_token=")[-1].split(";")[0]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get("email")
    history = get_last_message(50)
    for msg in history:
        await websocket.send_text(f"{msg.sender_email}: {msg.content}")
    try:
        # Ожидаем сообщения от клиента
        while True:
            data = await websocket.receive_text()  # Получаем текстовое сообщение от пользователя
            save_message(sender_email=user_email, content=data)
            await manager.broadcast(f"{user_email}: {data}")  # Рассылаем сообщение всем подключенным
    except WebSocketDisconnect:
        # Обрабатываем отключение клиента
        manager.disconnect(websocket)
        await manager.broadcast(f"Пользователь {user_email} покинул чат.")