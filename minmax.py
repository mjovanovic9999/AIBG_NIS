from copy import deepcopy
from functools import cache
from telnetlib import NEW_ENVIRON
from constants import ALPHA_START, BETA_START, COMMANDO_PLACE_MATRIX, GUNNER, GUNNER_PLACE_MATRIX, INFANTRY, INFANTRY_ATTACK_MATRIX, INFANTRY_PLACE_MATRIX, MORTAR, MORTAR_PLACE_MATRIX
from heuristic import evaluate


@cache
def minmax(
    state,
    depth,
    on_turn_max,
    on_turn_min,
    is_player_min=False,
    alpha=(ALPHA_START, None),
    beta=(BETA_START, None),
    my_move=None,
):  # vraca (value,new_state)
    if depth == 0:
        return
        # state,
        # depth,
        # is_player_min,
        # alpha,
        # beta,
        (evaluate(state, is_player_min if on_turn_min else on_turn_max), my_move)

    if is_player_min:
        for new_state in generate_next_states(state, on_turn_max, on_turn_min, True):
            beta = min(
                beta,
                minmax(
                    new_state,
                    depth-1,
                    on_turn_max,
                    on_turn_min,
                    False,
                    alpha,
                    beta,
                    new_state if my_move is None else my_move
                ),
                key=lambda x: x[0])
            if alpha[0] >= beta[0]:
                return alpha
        return beta

    else:  # maxplayer
        for new_state in generate_next_states(state, on_turn_max, on_turn_min, False):
            alpha = max(
                alpha,
                minmax(
                    new_state,
                    depth-1,
                    on_turn_max,
                    on_turn_min,
                    True,
                    alpha,
                    beta,
                    new_state if my_move is None else my_move
                ),
                key=lambda x: x[0])
            if alpha[0] >= beta[0]:
                return beta
        return alpha


def generate_next_states(state, on_turn_max, on_turn_min, is_player_min):
    #generate_all_moves pa filtrirati validne poteze
    pass

def generate_all_moves(state, on_turn_max, on_turn_min, is_player_min):
    on_turn=on_turn_min if is_player_min else on_turn_max

    my_figures_indexes=[]
    new_states=[]

    for index,figure in state:
        if figure["playerID"]== on_turn:
            my_figures_indexes.append(index)

    for index in my_figures_indexes:
        
        if state[index]["figureType"]==INFANTRY:
            for position in INFANTRY_PLACE_MATRIX:#moves
                #da l je validan potez tu

                new_states.append(deepcopy(state))        
                new_states[-1][index]["coordX"]+=position[0]
                new_states[-1][index]["coordY"]+=position[1]
            
            for attack in INFANTRY_ATTACK_MATRIX:
                pass#isAttacked


            
        elif figure["figureType"]==GUNNER:
            for position in GUNNER_PLACE_MATRIX:
                #da l je validan potez tu

                new_states.append(deepcopy(state))        
                new_states[-1][index]["coordX"]+=position[0]
                new_states[-1][index]["coordY"]+=position[1]
        elif figure["figureType"]==MORTAR:
            for position in MORTAR_PLACE_MATRIX:
                #da l je validan potez tu

                new_states.append(deepcopy(state))        
                new_states[-1][index]["coordX"]+=position[0]
                new_states[-1][index]["coordY"]+=position[1]
        else:
            for position in COMMANDO_PLACE_MATRIX:
                #da l je validan potez tu

                new_states.append(deepcopy(state))        
                new_states[-1][index]["coordX"]+=position[0]
                new_states[-1][index]["coordY"]+=position[1]
    
        #attacks

