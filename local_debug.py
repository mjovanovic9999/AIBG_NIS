from constants import GUNNER,MORTAR,COMMANDO,INFANTRY
from helpers import print_table,gen_table_state_with_empty_positions

init_state = [
        {"coordX": 0,"coordY": 2, "figureType": GUNNER, "playerID": "1"} ,
        {"coordX": 0,"coordY": 4, "figureType": MORTAR, "playerID": "1"},
        {"coordX": 0,"coordY": 6, "figureType": COMMANDO, "playerID": "1"},
        {"coordX": 0,"coordY": 8, "figureType": GUNNER, "playerID": "1"},
        {"coordX": 2,"coordY": 2, "figureType": INFANTRY, "playerID": "1" },
        {"coordX": 2,"coordY": 4, "figureType": INFANTRY, "playerID": "1" },
        {"coordX": 2,"coordY": 6, "figureType": INFANTRY, "playerID": "1"},
        {"coordX": 2,"coordY": 8, "figureType": INFANTRY, "playerID": "1" },

        {"coordX": 10,"coordY": 2, "figureType": INFANTRY, "playerID": "2"} ,
        {"coordX": 10,"coordY": 4, "figureType": INFANTRY, "playerID": "2"},
        {"coordX": 10,"coordY": 6, "figureType": INFANTRY, "playerID": "2"},
        {"coordX": 10,"coordY": 8, "figureType": INFANTRY, "playerID": "2"},
        {"coordX": 12,"coordY": 2, "figureType": GUNNER, "playerID": "2"},
        {"coordX": 12,"coordY": 4, "figureType": COMMANDO , "playerID": "2"},
        {"coordX": 12,"coordY": 6, "figureType": MORTAR, "playerID": "2"},
        {"coordX": 12,"coordY": 8, "figureType": GUNNER, "playerID": "2"}
]

def start_game():
    minimax_depth=3
    state=init_state
    print_table(gen_table_state_with_empty_positions(state))
    


start_game()
