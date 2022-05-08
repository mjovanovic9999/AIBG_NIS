from typing import Any
import socketio
import requests

from constants import MINMAX_DEPTH
from minmax import minmax


def init_connection(game_state: dict[str, Any]):
    sio = socketio.Client(logger=True, engineio_logger=True)

    add_event_handlers(sio, game_state)

    ime = input("Ime")
    sio.connect("http://localhost:3001")

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
    def yourTurn(table_state: list[dict[str, Any]]):
        #print("Your turn!")
        #print_table(table_state, game_state["botID"])
        game_state["table_state"] = table_state
        
        #print(table_state)

        for position in table_state:
            if position["playerID"] != game_state["botID"]:
              #  print(position["botID"])
                submit_move(minmax((table_state, None), MINMAX_DEPTH, game_state["botID"], position["playerID"])[1])
                break

    @sio.event
    def readyToBattle(bot_id: str):
        print("Ready to battle!")
        game_state["botID"] = bot_id


def validate_move(move: dict[str, Any]) -> bool:
    return bool(requests.post("http://localhost:3001/validateAction", json=move).text)


def submit_move(move: dict[str, Any]) -> None:
    requests.post("http://localhost:3001/doAction", json=move)
