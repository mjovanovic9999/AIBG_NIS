from copy import deepcopy
from queue import Queue
from constants import ALPHA_START, BETA_START, COMMANDO, COMMANDO_ATTACK_MATRIX, COMMANDO_PLACE_MATRIX, GUNNER, GUNNER_PLACE_MATRIX, INFANTRY, INFANTRY_ATTACK_MATRIX, INFANTRY_PLACE_MATRIX, MORTAR, MORTAR_PLACE_MATRIX
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
        return (evaluate(state[0], on_turn_min if is_player_min else on_turn_max), my_move)

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

# def iterative_deepening(
#     state,
#     depth,
#     on_turn_max,
#     on_turn_min,
#     is_player_min=False,
#     alpha=(ALPHA_START, None),
#     beta=(BETA_START, None),
#     my_move=None,
# ):
#     return


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
        return (evaluate(state, on_turn_min if is_player_min else on_turn_max), my_move)

    new_states = generate_next_states(state, on_turn_max, on_turn_min, True)
 
    for new_state in new_states:
        if new_state == new_states[0]:
            score = pvs(state, depth-1, on_turn_max, on_turn_min,
                                not is_player_min, -beta, -alpha,
                                new_state[1] if my_move is None else my_move)
        else:
            score = pvs(state, depth-1, on_turn_max, on_turn_min,
                                not is_player_min, -alpha-1, -alpha,
                                new_state[1] if my_move is None else my_move)

            if alpha < score and score < beta:
                score = pvs(state, depth-1, on_turn_max, on_turn_min,
                                    not is_player_min, -beta, -score,
                                    new_state[1] if my_move is None else my_move)
        alpha = max(alpha, score, key=lambda x: x[0])

        if alpha[0] >= beta[0]:
            return beta
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
    on_turn = on_turn_min if is_player_min else on_turn_max

    my_figures_indexes = []
    opponent_figures_indexes = []
    new_states = []

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
                new_states.append((deepcopy(state[0]), form_action(
                    0, (state[0][index]["coordX"], state[0][index]["coordY"]), on_turn, move, state[0][index]["figureType"])))
                new_states[-1][0][index]["coordX"] = move[0]
                new_states[-1][0][index]["coordY"] = move[1]

        elif figure["figureType"] == GUNNER:
            posible_positions = generate_figure_moves(
                state[0], state[0][index], GUNNER, GUNNER_PLACE_MATRIX)
            for move in posible_positions:
                new_states.append((deepcopy(state[0]), form_action(
                    0, (state[0][index]["coordX"], state[0][index]["coordY"]), on_turn, move, state[0][index]["figureType"])))
                new_states[-1][0][index]["coordX"] = move[0]
                new_states[-1][0][index]["coordY"] = move[1]

        elif figure["figureType"] == MORTAR:
            posible_positions = generate_figure_moves(
                state[0], state[0][index], MORTAR, MORTAR_PLACE_MATRIX)
            for move in posible_positions:
                new_states.append((deepcopy(state[0]), form_action(
                    0, (state[0][index]["coordX"], state[0][index]["coordY"]), on_turn, move, state[0][index]["figureType"])))
                new_states[-1][0][index]["coordX"] = move[0]
                new_states[-1][0][index]["coordY"] = move[1]
        else:
            posible_positions = generate_figure_moves(
                state[0], state[0][index], COMMANDO, COMMANDO_PLACE_MATRIX)
            for move in posible_positions:
                new_states.append((deepcopy(state[0]), form_action(
                    0, (state[0][index]["coordX"], state[0][index]["coordY"]), on_turn, move, state[0][index]["figureType"])))
                new_states[-1][0][index]["coordX"] = move[0]
                new_states[-1][0][index]["coordY"] = move[1]

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

    if commando_index:
        for opponent_index in opponent_figures_indexes:
            if is_attacked(state[0][commando_index], state[0][opponent_index], state[0]):

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

    return new_states


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
