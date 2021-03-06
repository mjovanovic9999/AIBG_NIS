import time
from constants import GUNNER, MINMAX_DEPTH,MORTAR,COMMANDO,INFANTRY
from helpers import print_table,gen_table_state_with_empty_positions
from minmax import minmax

init_state = [
        {"coordX": 0,"coordY": 2, "figureType": GUNNER, "playerID": "1"} ,
        {"coordX": 0,"coordY": 4, "figureType": MORTAR, "playerID": "1"},
        {"coordX": 9,"coordY": 5, "figureType": COMMANDO, "playerID": "1"},
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
    minimax_depth=MINMAX_DEPTH
    state=init_state
    print_table(gen_table_state_with_empty_positions(state),"1")
    while True:
        old_time=time.time()
        heur,move=minmax((state,None),minimax_depth,"1","2")
        print(time.time()-old_time)
        print(heur)
        print(move)
        play_move(state,move)
        print_table(gen_table_state_with_empty_positions(state),"1")

        old_time=time.time()
        heur,move=minmax((state,None),minimax_depth,"2","1")
        print(time.time()-old_time)

        print(heur)
        print(move)
        play_move(state,move)
        print_table(gen_table_state_with_empty_positions(state),"1")



start_game()
