from typing import Any

def print_table(table_state: list[dict[str, Any]]) -> None:
    char_to_print = ""
    first_player_id = "1"
    table = ""
    

    for i in range(13):

        for j in range(11):
            figureType = table_state[i * 11 +j]["figureType"]
            if figureType == -1:
                char_to_print = "--"
            else:
                # if not first_player_id:
                #     first_player_id = table_state[i * 11 +j]["playerID"]

                number_of_player = "1" if table_state[i * 11 +
                                                      j]["playerID"] == first_player_id else "2"
                if figureType == 0:
                    char_to_print = "I"
                elif figureType == 1:
                    char_to_print = "G"
                elif figureType == 2:
                    char_to_print = "M"
                else:
                    char_to_print = "C"
                char_to_print += number_of_player
            table += char_to_print
        table += "\n"
    
    print(table)


def gen_table_state_with_empty_positions(table_state: list[dict[str, Any]]) -> list[dict[str, Any]]:
    new_table_state = []
    for i in range(13):
        for j in range(11):
            filtered_position = list(filter(
                lambda position: position["coordX"] == i and position["coordY"] == j, table_state))
            new_table_state.append(filtered_position[0] if filtered_position else {
                                   "coordX": i, "coordY": j, "figureType": -1, "playerID": "123"})
    return new_table_state
