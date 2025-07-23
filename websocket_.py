import json
import asyncio
from fastapi import WebSocket, WebSocketException



def on_error(ws, error):
    print(f"There was an error occured {error}")

def on_open(ws):
    print("The websocket is now open.")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed", close_status_code, close_msg)


class websocket_manager:
    def __init__(self):
        self.active_connection: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)
    
    async def send_to(self, message, websocket: WebSocket):
        await websocket.send_text(message)

        



