from copy import deepcopy
from functools import cache
from queue import Queue
from constants import ALPHA_START, BETA_START, COMMANDO, COMMANDO_PLACE_MATRIX, GUNNER, GUNNER_PLACE_MATRIX, INFANTRY, INFANTRY_ATTACK_MATRIX, INFANTRY_PLACE_MATRIX, MORTAR, MORTAR_PLACE_MATRIX
from heuristic import evaluate, is_attacked, is_free, possible_moves


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
):  # vraca (value,new_state,move)
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
            posible_positions = generate_figure_moves(
                state, state[index], INFANTRY, INFANTRY_PLACE_MATRIX)
            for move in posible_positions:
                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] = move[0]
                new_states[-1][index]["coordY"] = move[1]

        elif figure["figureType"] == GUNNER:
            posible_positions = generate_figure_moves(
                state, state[index], GUNNER, GUNNER_PLACE_MATRIX)
            for move in posible_positions:
                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] = move[0]
                new_states[-1][index]["coordY"] = move[1]

        elif figure["figureType"] == MORTAR:
            posible_positions = generate_figure_moves(
                state, state[index], MORTAR, MORTAR_PLACE_MATRIX)
            for move in posible_positions:
                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] = move[0]
                new_states[-1][index]["coordY"] = move[1]
        else:
            posible_positions = generate_figure_moves(
                state, state[index], COMMANDO, COMMANDO_PLACE_MATRIX)
            for move in posible_positions:
                new_states.append(deepcopy(state))
                new_states[-1][index]["coordX"] = move[0]
                new_states[-1][index]["coordY"] = move[1]

    # attacks
    attacked_opponent_indexes = []
    commando_index = None
    # optimizacija jer napadnute pozicije se mnogo malo razlikuju izmedju stanja
    for opponent_index in opponent_figures_indexes:
        for index in my_figures_indexes:
            if state[index]["figureType"] == COMMANDO:
                commando_index = index
                continue

            if is_attacked(state[index], state[opponent_index], state):
                attacked_opponent_indexes.append(opponent_index)
                break

    for oppoenet_to_eat in attacked_opponent_indexes:
        new_states.append(deepcopy(state))
        del new_states[-1][oppoenet_to_eat]

    if commando_index:
        for opponent_index in opponent_figures_indexes:
            if is_attacked(state[commando_index], state[opponent_index], state):
                new_states.append(deepcopy(state))

                new_states[-1][commando_index]["coordX"] = state[opponent_index]["coordX"]
                new_states[-1][commando_index]["coordY"] = state[opponent_index]["coordY"]

                del new_states[-1][opponent_index]

    return new_states


def generate_figure_moves(game_state, figure, fig_type, fig_move_matrix):
    all_moves = set()
    if(figure["figureType"] == fig_type):
        origin = (figure["coordX"], figure["coordY"])
        q = Queue()
        q.put(origin)
        while q:
            pos = q.get()
            for x in range(-1, 2):
                for y in range(-1, 2):
                    new_pos = (pos[0]+x, pos[1]+y)
                    if x != new_pos[0] and y != new_pos[1] and new_pos != origin and 13 > new_pos[0] > -1 and 11 > new_pos[1] > -1 and is_free(game_state, new_pos[0], new_pos[1]) and (new_pos[0]-origin[0], new_pos[1]-origin[1]) in fig_move_matrix:
                        if new_pos not in all_moves:
                            all_moves.add(new_pos)
                            q.put(new_pos)
    return all_moves

def can_commando_attack(game_state,figure,victim):
    all_moves=set()
    if(figure["figureType"]==COMMANDO):
        origin=(figure["coordX"],figure["coordY"])
        q=Queue()
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

