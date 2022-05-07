from typing import Any
from connection import init_connection


# game_state=[{ "coordX": 0, "coordY": 0, "figureType": 0, "playerID": "123"},
#             { "coordX": 1, "coordY": 2, "figureType": 2, "playerID": "" },
#             { "coordX": 1, "coordY": 3, "figureType": 1, "playerID": "123" }]


def main():
    game_state = {"botID": "", "table_state": []}
    init_connection(game_state)
