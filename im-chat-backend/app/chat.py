from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict
from .models import Message, ChatRoom, active_connections, chat_rooms
from .auth import get_current_user
import json

class ConnectionManager:
    def __init__(self):
        pass

    async def connect(self, websocket: WebSocket, room: str, username: str):
        await websocket.accept()
        if room not in active_connections:
            active_connections[room] = {}
        active_connections[room][username] = websocket
        if room not in chat_rooms:
            chat_rooms[room] = ChatRoom(name=room)
        if username not in chat_rooms[room].participants:
            chat_rooms[room].participants.append(username)

    async def disconnect(self, room: str, username: str):
        if room in active_connections and username in active_connections[room]:
            del active_connections[room][username]
            if username in chat_rooms[room].participants:
                chat_rooms[room].participants.remove(username)

    async def broadcast(self, message: Message, room: str):
        if room in active_connections:
            chat_rooms[room].messages.append(message)
            for connection in active_connections[room].values():
                await connection.send_text(json.dumps(message.dict()))

manager = ConnectionManager()
