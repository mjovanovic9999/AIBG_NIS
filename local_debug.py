from constants import GUNNER,MORTAR,COMMANDO,INFANTRY
from helpers import print_table,gen_table_state_with_empty_positions
from minmax import minmax
from copy import deepcopy
from connection import validate_move

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

def play_move(state,move):
    for_validation=deepcopy(move)
    for_validation["GB"]=state
    #print(validate_move(for_validation))
    #VALIDATORAAT
    toremove=dict()
    if(move["type"]==0):
        for figure in state:
            if figure["coordX"]==move["figureCoords"]["x"] and figure["coordY"]==move["figureCoords"]["y"]:
                figure["coordX"]=move["targetCoords"]["x"]
                figure["coordY"]=move["targetCoords"]["y"]
    else:
        for figure in state:
            if figure["coordX"]==move["targetCoords"]["x"] and figure["coordY"]==move["targetCoords"]["y"]:
                toremove=figure
        if move["figureType"]==COMMANDO:
            figure["coordX"]=move["targetCoords"]["x"]
            figure["coordY"]=move["targetCoords"]["y"]
    if toremove:
        state.remove(toremove)

def start_game():
    minimax_depth=2
    state=init_state
    print_table(gen_table_state_with_empty_positions(state))
    while True:
        heur,move=minmax((state,None),minimax_depth,"1","2")
        print(heur)
        print(move)
        play_move(state,move)
        print_table(gen_table_state_with_empty_positions(state))

        heur,move=minmax((state,None),minimax_depth,"2","1")
        play_move(state,move)
        print_table(gen_table_state_with_empty_positions(state))



start_game()
