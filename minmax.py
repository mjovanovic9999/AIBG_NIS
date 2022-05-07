from heuristic import heuristic


def minmax(
    state,
    depth,
    is_player_min,
    alpha,
    beta,
    #my_move,
):
    if depth == 0:
        return (state, depth, is_player_min, alpha, beta, heuristic(state))

    for new_state in generate_next_states(state, is_player_min):
        pass




    return None


def generate_next_states(state, is_player_min):
    pass
