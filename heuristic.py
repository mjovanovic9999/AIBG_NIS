from math import sqrt
import constants
from validators import is_attacked

def get_figure_value(figure:dict):
    if(figure["figureType"]==constants.INFANTRY):
        return 100
    elif(figure["figureType"]==constants.GUNNER):
        return 125
    elif (figure["figureType"] == constants.MORTAR):
        return 150
    elif (figure["figureType"] == constants.COMMANDO):
        return 200

def evaluate(game_state:list,on_turn:str):
    fig_shift=9
    att_shift=4
    bait_shift=2
    pos_shift = 1
    setAttacking = set()

    value=0

    for figure in game_state:
        figure_val=get_figure_value(figure)

        if(figure["playerID"]==on_turn):
            #moja figura
            value+=figure_val<<fig_shift
            '''
            is_defended=False
            for ally in game_state:
                if ally["playerID"]==on_turn and ally!=figure and is_attacked(ally,figure,game_state):
                    is_defended=True
            '''

            for opponent in game_state:
                if opponent["playerID"]!=on_turn and is_attacked(opponent,figure,game_state):
                    '''
                    if opponent["figureType"]==constants.COMMANDO:
                        if is_defended:
                            value+=figure_val<<bait_shift
                        else:
                            value-=figure_val<<att_shift
                    else:
                    '''
                    value-=figure_val<<att_shift
        else:
            value-=figure_val<<fig_shift
            '''
            is_defended=False
            for ally in game_state:
                if ally["playerID"]==on_turn and ally!=figure and is_attacked(ally,figure,game_state):
                   is_defended=True
            '''
            #zapravo moj
            for ally in game_state:
                if ally["playerID"]!=on_turn and is_attacked(ally,figure,game_state):
                        '''
                    if ally["figureType"]==constants.COMMANDO:
                        if not is_defended:
                            value+=figure_val<<att_shift
                    else:
                        '''
                        value+=figure_val<<att_shift

        #pozicija
        if(figure["playerID"] == on_turn):
            if (figure["figureType"] == constants.INFANTRY):
                for positions in constants.INFANTRY_ATTACK_MATRIX:
                    if -1<figure["coordX"]+positions[0]<13 and -1<figure["coordY"]+positions[1]<11:
                        setAttacking.add((figure["coordX"]+positions[0],figure["coordY"]+positions[1]))
            if(figure["figureType"] == constants.GUNNER):
                for positions in constants.GUNNER_ATTACK_MATRIX:
                    if -1<figure["coordX"]+positions[0]<13 and -1<figure["coordY"]+positions[1]<11:
                        setAttacking.add((figure["coordX"]+positions[0],figure["coordY"]+positions[1]))
            if(figure["figureType"] == constants.MORTAR):
                for positions in constants.MORTAR_ATTACK_MATRIX:
                    if -1<figure["coordX"]+positions[0]<13 and -1<figure["coordY"]+positions[1]<11:
                        setAttacking.add((figure["coordX"]+positions[0],figure["coordY"]+positions[1]))
            if(figure["figureType"] == constants.COMMANDO):
                for positions in constants.COMMANDO_ATTACK_MATRIX:
                    if -1<figure["coordX"]+positions[0]<13 and -1<figure["coordY"]+positions[1]<11:
                        setAttacking.add((figure["coordX"]+positions[0],figure["coordY"]+positions[1]))
        value += len(setAttacking)<<pos_shift

    return value
