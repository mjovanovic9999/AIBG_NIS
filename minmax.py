import bisect
from copy import deepcopy
from queue import Queue
from constants import ALPHA_START, BETA_START, COMMANDO, COMMANDO_ATTACK_MATRIX, COMMANDO_PLACE_MATRIX, CUTOFF, GUNNER, GUNNER_PLACE_MATRIX, INFANTRY, INFANTRY_ATTACK_MATRIX, INFANTRY_PLACE_MATRIX, MORTAR, MORTAR_PLACE_MATRIX
from heuristic import evaluate
from validators import is_attacked, is_free


def minmax(
    state,
    depth,
    on_turn_max,
    on_turn_min,
    is_player_min=False,
    alpha=(ALPHA_START, None),
    beta=(BETA_START, None),
    my_move=None,
):  # vraca (value,move)
    if depth == 0:  # mat
        return (evaluate(state[0], on_turn_min if is_player_min else on_turn_max) * (-1 if is_player_min else 1) , my_move)

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
                    new_state[1] if my_move is None else my_move
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
                    new_state[1] if my_move is None else my_move
                ),
                key=lambda x: x[0])
            if alpha[0] >= beta[0]:
                return beta
        return alpha


def minmax_dict(
    state,
    depth,
    on_turn_max,
    on_turn_min,
    is_player_min=False,
    alpha=(ALPHA_START, None),
    beta=(BETA_START, None),
    my_move=None,
    state_dict=None,
):  # vraca (value,move)
    if depth == 0:  # mat
        return (evaluate(state[0], on_turn_min if is_player_min else on_turn_max) *(-1 if is_player_min else 1) , my_move)

    if is_player_min:
        new_states = generate_next_states(
            state, on_turn_max, on_turn_min, True)

        state_dict[depth] = new_states

        for new_state in new_states:
            beta = min(
                beta,
                minmax_dict(
                    new_state,
                    depth-1,
                    on_turn_max,
                    on_turn_min,
                    False,
                    alpha,
                    beta,
                    new_state[1] if my_move is None else my_move,
                    state_dict
                ),
                key=lambda x: x[0])
            if alpha[0] >= beta[0]:
                return alpha
        return beta

    else:  # maxplayer
        new_states = generate_next_states(
            state, on_turn_max, on_turn_min, False)

        state_dict[depth] = new_states

        for new_state in new_states:
            alpha = max(
                alpha,
                minmax_dict(
                    new_state,
                    depth-1,
                    on_turn_max,
                    on_turn_min,
                    True,
                    alpha,
                    beta,
                    new_state[1] if my_move is None else my_move,
                    state_dict
                ),
                key=lambda x: x[0])
            if alpha[0] >= beta[0]:
                return beta
        return alpha


def pvs(
    state,
    depth,
    on_turn_max,
    on_turn_min,
    is_player_min=False,
    alpha=(ALPHA_START, None),
    beta=(BETA_START, None),
    my_move=None,
):  # vraca (value,move)
    if depth == 0:
        return (evaluate(state[0], on_turn_min if is_player_min else on_turn_max) *(-1 if is_player_min else 1) , my_move)


    new_states = generate_next_states(state, on_turn_max, on_turn_min, is_player_min)

    for new_state in new_states:
        if new_state == new_states[0]:
            tmp = pvs(new_state, depth-1, on_turn_max, on_turn_min,
                      not is_player_min, (-beta[0],
                                          beta[1]), (-alpha[0], alpha[1]),
                      new_state[1] if my_move is None else my_move)
            score = (-tmp[0], tmp[1])
        else:
            tmp = pvs(new_state, depth-1, on_turn_max, on_turn_min,
                      not is_player_min, (-alpha[0]-1,
                                          alpha[1]), (-alpha[0], alpha[1]),
                      new_state[1] if my_move is None else my_move)
            score = (-tmp[0], tmp[1])

            if alpha[0] < score[0] and score[0] < beta[0]:
                tmp = pvs(state, depth-1, on_turn_max, on_turn_min,
                          not is_player_min, (-beta[0],
                                              beta[1]), (-score[0], score[1]),
                          new_state[1] if my_move is None else my_move)
                score = (-tmp[0], tmp[1])
        alpha = max(alpha, score, key=lambda x: x[0])

        if alpha[0] >= beta[0]:
            break
    return alpha


def form_action(type, figure_coords: tuple, id, target: tuple, figure_type):
    action = {
        "type": type,
        'figureCoords': {'x': figure_coords[0], 'y': figure_coords[1]},
        'playerID': id,
        'targetCoords': {'x': target[0], 'y': target[1]},
        'figureType': figure_type
    }
    return action


def generate_next_states(state, on_turn_max, on_turn_min, is_player_min):
    max_states=CUTOFF

    on_turn = on_turn_min if is_player_min else on_turn_max

    my_figures_indexes = []
    opponent_figures_indexes = []
    new_states = []

    best_values=list()

    action = {'type': 1, 'figureCoords': {'x': 1, 'y': 2},
              'playerID': '123', 'targetCoords': {'x': 1, 'y': 2}, 'figureType': 0}

    for index, figure in enumerate(state[0]):
        if figure["playerID"] == on_turn:
            my_figures_indexes.append(index)
        else:
            opponent_figures_indexes.append(index)

    # moves
    for index in my_figures_indexes:

        if state[0][index]["figureType"] == INFANTRY:
            posible_positions = generate_figure_moves(
                state[0], state[0][index], INFANTRY, INFANTRY_PLACE_MATRIX)
            for move in posible_positions:
                add_movement(new_states,index,state,move,on_turn,best_values,max_states,is_player_min)

        elif figure["figureType"] == GUNNER:
            posible_positions = generate_figure_moves(
                state[0], state[0][index], GUNNER, GUNNER_PLACE_MATRIX)
            for move in posible_positions:
                add_movement(new_states,index,state,move,on_turn,best_values,max_states,is_player_min)

        elif figure["figureType"] == MORTAR:
            posible_positions = generate_figure_moves(
                state[0], state[0][index], MORTAR, MORTAR_PLACE_MATRIX)
            for move in posible_positions:
                add_movement(new_states,index,state,move,on_turn,best_values,max_states,is_player_min)
        else:
            posible_positions = generate_figure_moves(
                state[0], state[0][index], COMMANDO, COMMANDO_PLACE_MATRIX)
            for move in posible_positions:
                add_movement(new_states,index,state,move,on_turn,best_values,max_states,is_player_min)

    # attacks
    eating_pair_indexes = []  # tuple(index protivik,my index)
    commando_index = None
    # optimizacija jer napadnute pozicije se mnogo malo razlikuju izmedju stanja
    for opponent_index in opponent_figures_indexes:
        for index in my_figures_indexes:
            if state[0][index]["figureType"] == COMMANDO:
                commando_index = index
                continue

            if is_attacked(state[0][index], state[0][opponent_index], state[0]):
                eating_pair_indexes.append((opponent_index, index))
                break

    for eating_pair in eating_pair_indexes:
        add_attack(new_states,state,eating_pair,on_turn,best_values,max_states,is_player_min)

    if commando_index:
        for opponent_index in opponent_figures_indexes:
            if is_attacked(state[0][commando_index], state[0][opponent_index], state[0]):
                add_commando_attack(new_states,state,commando_index,on_turn,opponent_index,best_values,max_states,is_player_min)
    state_cleanup(is_player_min,best_values,new_states,on_turn)
    return [x[0] for x in new_states]

def state_cleanup(is_player_min,best_values,new_states,on_turn):
    to_remove=list()
    for state in new_states:
        if is_player_min:
            if state[1]>best_values[-1]:
                to_remove.append(state)
        else:
            if state[1]<best_values[0]:
                to_remove.append(state)
    for s in to_remove:
        new_states.remove(s)

def state_insert(is_player_min,best_values,max_states,new_states,on_turn):
    if is_player_min:
        eval=-evaluate(new_states[-1][0],on_turn)
        new_states.append((new_states[-1],eval))
        new_states.remove(new_states[-2])
        if len(best_values)<max_states:
            bisect.insort(best_values,eval)
        elif eval<best_values[-1]:
            bisect.insort(best_values,eval)
            best_values.remove(best_values[-1])
        else:
            new_states.remove(new_states[-1])
    else:
        eval=evaluate(new_states[-1][0],on_turn)
        new_states.append((new_states[-1],eval))
        new_states.remove(new_states[-2])
        if len(best_values)<max_states:
            bisect.insort(best_values,eval)
        elif eval>best_values[0]:
            bisect.insort(best_values,eval)
            best_values.remove(best_values[0])
        else:
            new_states.remove(new_states[-1])

def add_movement(new_states,index,state,move,on_turn,best_values,max_states,is_player_min):
    new_states.append((deepcopy(state[0]), form_action(
        0, (state[0][index]["coordX"], state[0][index]["coordY"]), on_turn, move, state[0][index]["figureType"])))
    new_states[-1][0][index]["coordX"] = move[0]
    new_states[-1][0][index]["coordY"] = move[1]
    state_insert(is_player_min,best_values,max_states,new_states,on_turn)
    

def add_attack(new_states,state,eating_pair,on_turn,best_values,max_states,is_player_min):
    new_states.append(
        (deepcopy(state[0]),
            form_action(1,
            (state[0][eating_pair[1]]["coordX"],
            state[0][eating_pair[1]]["coordY"]),
            on_turn,
            (state[0][eating_pair[0]]["coordX"],
                state[0][eating_pair[0]]["coordY"]),
            state[0][eating_pair[1]]["figureType"]))
    )
    # new_states.append(deepcopy(state[0]))
    del new_states[-1][0][eating_pair[0]]
    state_insert(is_player_min,best_values,max_states,new_states,on_turn)

def add_commando_attack(new_states,state,commando_index,on_turn,opponent_index,best_values,max_states,is_player_min):
    new_states.append(
        (deepcopy(state[0]),
            form_action(1,
                        (state[0][commando_index]["coordX"],
                        state[0][commando_index]["coordY"]),
                        on_turn,
                        (state[0][opponent_index]["coordX"],
                            state[0][opponent_index]["coordY"]),
                        commando_index))
    )

    new_states[-1][0][commando_index]["coordX"] = state[0][opponent_index]["coordX"]
    new_states[-1][0][commando_index]["coordY"] = state[0][opponent_index]["coordY"]

    del new_states[-1][0][opponent_index]
    state_insert(is_player_min,best_values,max_states,new_states,on_turn)

def generate_figure_moves(game_state, figure, fig_type, fig_move_matrix):
    all_moves = set()
    if(figure["figureType"] == fig_type):
        origin = (figure["coordX"], figure["coordY"])
        q = Queue(24)
        q.put(origin)
        while not q.empty():
            pos = q.get()
            for x in range(-1, 2):
                for y in range(-1, 2):
                    new_pos = (pos[0]+x, pos[1]+y)
                    if new_pos != pos and new_pos != origin and 13 > new_pos[0] > -1 and 11 > new_pos[1] > -1:
                        if is_free(game_state, new_pos[0], new_pos[1]):
                            if (new_pos[0]-origin[0], new_pos[1]-origin[1]) in fig_move_matrix:
                                if new_pos not in all_moves:
                                    all_moves.add(new_pos)
                                    q.put(new_pos)
    return all_moves
