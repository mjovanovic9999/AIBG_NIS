from socket import socket
from typing import Any
import socketio
import requests


def init_connection(game_state: dict[str, Any]):
    sio = socketio.Client()

    add_event_handlers(sio, game_state)

    sio.connect("")

    sio.emit('setName', "Klika010")

    sio.wait()


def add_event_handlers(sio: socketio.Client, game_state: dict[str, Any]) -> None:
    @sio.event
    def connect():
        print("I'm connected!")

    @sio.event
    def connect_error(data):
        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")

    @sio.event
    def yourTurn(table_state: dict[str,Any]):
        game_state["table_state"] = table_state

    @sio.event
    def readyToBattle(bot_id: str):
        game_state["botID"] = bot_id


def validate_move(move: dict[str, Any]) -> bool:
    return bool(requests.post("http://localhost:3000/validateAction", json=move).text)

def submit_move() -> None:
    return