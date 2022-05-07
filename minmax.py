from copy import deepcopy
from functools import cache
import queue
from telnetlib import NEW_ENVIRON
from constants import ALPHA_START, BETA_START, COMMANDO, COMMANDO_ATTACK_MATRIX, COMMANDO_PLACE_MATRIX, GUNNER, GUNNER_PLACE_MATRIX, INFANTRY, INFANTRY_ATTACK_MATRIX, INFANTRY_PLACE_MATRIX, MORTAR, MORTAR_PLACE_MATRIX
from heuristic import evaluate, is_attacked,is_free


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
    # generate_all_moves pa filtrirati validne poteze
    pass


def generate_all_moves(state, on_turn_max, on_turn_min, is_player_min):
    on_turn = on_turn_min if is_player_min else on_turn_max

    my_figures_indexes = []
    opponent_figures_indexes = []
    new_states = []

    for index, figure in state:
        if figure["playerID"] == on_turn:
            my_figures_indexes.append(index)
        else:
            opponent_figures_indexes.append(index)
    # moves
    for index in my_figures_indexes:

        if state[index]["figureType"] == INFANTRY:
                ########

                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] += position[0]
                new_states[-1][index]["coordY"] += position[1]

        elif figure["figureType"] == GUNNER:
            for position in GUNNER_PLACE_MATRIX:
                # da l je validan potez tu

                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] += position[0]
                new_states[-1][index]["coordY"] += position[1]
        elif figure["figureType"] == MORTAR:
            for position in MORTAR_PLACE_MATRIX:
                # da l je validan potez tu

                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] += position[0]
                new_states[-1][index]["coordY"] += position[1]
        else:
            for position in COMMANDO_PLACE_MATRIX:
                # da l je validan potez tu

                # to je ujedno i napad commando
                # dodatno izbaiti iz niz

                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] += position[0]
                new_states[-1][index]["coordY"] += position[1]

    # attacks
    attacked_opponent_indexes = []
    # optimizacija jer napadnute pozicije se mnogo malo razlikuju izmedju stanja
    for opponent_index in opponent_figures_indexes:
        for index in my_figures_indexes:
            if is_attacked(state[index], state[opponent_index], state):
                attacked_opponent_indexes.append(opponent_index)
                break

    for oppoenet_to_eat in attacked_opponent_indexes:
        new_states.append(deepcopy(state))
        del new_states[-1][oppoenet_to_eat]


def generate_figure_moves(game_state,figure,fig_type,fig_move_matrix):
    all_moves=set()
    if(figure["figureType"]==fig_type):
        origin=(figure["coordX"],figure["coordY"])
        q=queue.Queue()
        q.put(origin)
        while q:
            pos=q.get()
            for x in range(-1,2):
                for y in range(-1,2):
                    new_pos=(pos[0]+x,pos[1]+y)
                    if x!=new_pos[0] and y!=new_pos[1] and new_pos!=origin and 13>new_pos[0]>-1 and 11>new_pos[1]>-1 and is_free(game_state,new_pos[0],new_pos[1]) and (new_pos[0]-origin[0],new_pos[1]-origin[1]) in fig_move_matrix:
                        if new_pos not in all_moves:
                            all_moves.add(new_pos)
                            q.put(new_pos)
    return all_moves

def can_commando_attack(game_state,figure,victim):
    all_moves=set()
    if(figure["figureType"]==COMMANDO):
        origin=(figure["coordX"],figure["coordY"])
        q=queue.Queue()
        q.put(origin)
        while q:
            pos=q.get()
            for x in range(-1,2):
                for y in range(-1,2):
                    new_pos=(pos[0]+x,pos[1]+y)
                    if x!=new_pos[0] and y!=new_pos[1] and new_pos!=origin and 13>new_pos[0]>-1 and 11>new_pos[1]>-1 and (is_free(game_state,new_pos[0],new_pos[1]) or new_pos==victim) and (new_pos[0]-origin[0],new_pos[1]-origin[1]) in COMMANDO_ATTACK_MATRIX:
                        if new_pos not in all_moves:
                            if(new_pos==victim):
                                return True
                            all_moves.add(new_pos)
                            q.put(new_pos)
    return False

