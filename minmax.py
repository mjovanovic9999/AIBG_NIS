from functools import cache
from constants import ALPHA_START, BETA_START
from heuristic import heuristic


@cache
def minmax(
    state,
    depth,
    is_player_min,
    alpha=ALPHA_START,
    beta=BETA_START,
    # my_move,
):
    if depth == 0:
        return (
            # state,
            # depth,
            # is_player_min,
            # alpha,
            # beta,
            heuristic(state)
        )

    if is_player_min:
        for new_state in generate_next_states(state, is_player_min):
            beta = min(
                beta,
                minmax(
                    new_state,
                    depth-1,
                    False,
                    alpha,
                    beta

                )
            )
            if alpha >= beta:
                return alpha
        return beta

    else:  # maxplayer
        for new_state in generate_next_states(state, is_player_min):
            alpha = max(
                alpha,
                minmax(
                    new_state,
                    depth-1,
                    True,
                    alpha,
                    beta
                )
            )
            if alpha >= beta:
                return beta
        return alpha


def generate_next_states(state, is_player_min):
    pass
