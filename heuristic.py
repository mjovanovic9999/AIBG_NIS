from math import sqrt
import constants

def is_free(game_state:dict,x:int,y:int):
    for figure in game_state:
        if(figure["coordX"]==x and figure["coordY"]==y):
            return True
    return False

def dist_heuristic(a,b):
    return sqrt(a**2+b**2)

def possible_moves(game_state,origin,current):
    moves=[]
    for x_offset in range(-1,2):
        for y_offset in range(-1,2):
            diff=abs(current[0]+x_offset-origin[0])+abs(current[1]+y_offset-origin[1])
            new_pos=(current[0]+x_offset,current[1]+y_offset)
            if (x_offset!=0 and y_offset!=0) and diff<4 and is_free(game_state,new_pos[0],new_pos[1]) and 13>new_pos[0]>-1 and 11>new_pos[1]>-1:
                moves.append(new_pos)
    return moves

def commando_attack(attacker:dict, defender:dict, game_state:list):
    if(attacker["figureType"]==constants.COMMANDO):
        start=(attacker["coordX"],attacker["coordY"])
        end=(defender["coordX"],defender["coordY"])
        found_end = False
        open_set = set()
        open_set.add(start)
        closed_set = set()
        g = {}
        prev_nodes = {}
        g[start] = 0
        prev_nodes[start] = None
        while len(open_set) > 0 and (not found_end):
            node = None
            for next_node in open_set:
                if node is None or g[next_node] + dist_heuristic(next_node,end) < g[node] + dist_heuristic(node,end):
                    node = next_node
            if node == end:
                found_end = True
                break
            for m in possible_moves(game_state,start,node):
                if m not in open_set and m not in closed_set:
                    open_set.add(m)
                    prev_nodes[m] = node
                    g[m] = g[node] + 20
                else:
                    if g[m] > g[node] + 20:
                        g[m] = g[node] + 20
                        prev_nodes[m] = node
                        if m in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)
            open_set.remove(node)
            closed_set.add(node)
        path = []
        if found_end:
            return True
        else:
            return False
    else:
        return False

def is_attacked(attacker:dict, defender:dict, game_state:list):

    #Infantry
    if (attacker["figureType"] == constants.INFANTRY):

        #ista x koordinata
        if(attacker["coordX"]==defender["coordX"]):
            if(abs(attacker["coordY"]-defender["coordY"])==1):
                return True
            elif(attacker["coordY"]-defender["coordY"]==2 and is_free(game_state,attacker["coordX"],attacker["coordY"]-1)):
                return True
            elif(attacker["coordY"] - defender["coordY"] == -2 and is_free(game_state,attacker["coordX"],attacker["coordY"]+1)):
                return True

        #ista y koordinata
        if (attacker["coordY"] == defender["coordY"]):
            if (abs(attacker["coordX"] - defender["coordX"]) == 1):
                return True
            elif (attacker["coordX"] - defender["coordX"] == 2 and is_free(game_state, attacker["coordX"]-1,attacker["coordY"])):
                return True
            elif (attacker["coordX"] - defender["coordX"] == -2 and is_free(game_state, attacker["coordX"]+1,attacker["coordY"])):
                return True

    #Gunner
    elif (attacker["figureType"] == constants.GUNNER):
        diff=(abs(attacker["coordY"]-defender["coordY"])+abs(attacker["coordX"]-defender["coordX"]))
        if diff==2 or diff==3:
            if diff ==2:
                if(attacker["coordX"]==defender["coordX"]):
                    if is_free(game_state,attacker["coordX"],attacker["coordY"]-1) and attacker["coordY"]>defender["coordY"]:
                        return True
                    elif is_free(game_state,attacker["coordX"],attacker["coordY"]+1) and attacker["coordY"]<defender["coordY"]:
                        return True
                elif(attacker["coordY"] == defender["coordY"]):
                    if is_free(game_state,attacker["coordX"]-1,attacker["coordY"]) and attacker["coordX"]>defender["coordX"]:
                        return True
                    elif is_free(game_state,attacker["coordX"]+1,attacker["coordY"]) and attacker["coordX"] < defender["coordX"]:
                        return True
            elif diff == 3:
                #isto x
                if(attacker["coordX"]==defender["coordX"]):
                    if is_free(game_state,attacker["coordX"],attacker["coordY"]-1) and  is_free(game_state,attacker["coordX"],attacker["coordY"]-2) and attacker["coordY"]>defender["coordY"]:
                        return True
                    elif is_free(game_state,attacker["coordX"],attacker["coordY"]+1) and is_free(game_state,attacker["coordX"],attacker["coordY"]+2) and attacker["coordY"]<defender["coordY"]:
                        return True 
                #isto y
                elif(attacker["coordY"] == defender["coordY"]):
                    if is_free(game_state,attacker["coordX"]-1,attacker["coordY"]) and is_free(game_state,attacker["coordX"]-2,attacker["coordY"]) and attacker["coordX"]>defender["coordX"]:
                        return True
                    elif is_free(game_state,attacker["coordX"]+1,attacker["coordY"]) and is_free(game_state,attacker["coordX"]+2,attacker["coordY"]) and attacker["coordX"] < defender["coordX"]:
                        return True   
                #gore levo
                elif attacker["coordX"]>defender["coordX"] and attacker["coordY"]>defender["coordY"]:
                    if is_free(game_state,attacker["coordX"]-1,attacker["coordY"]-1):
                        return True
                #gore desno
                elif attacker["coordX"]>defender["coordX"] and attacker["coordY"]<defender["coordY"]:
                    if is_free(game_state,attacker["coordX"]-1,attacker["coordY"]+1):
                        return True
                #dole levo
                elif attacker["coordX"]<defender["coordX"] and attacker["coordY"]>defender["coordY"]:
                    if is_free(game_state,attacker["coordX"]+1,attacker["coordY"]-1):
                        return True
                #dole desno
                elif attacker["coordX"]<defender["coordX"] and attacker["coordY"]<defender["coordY"]:
                    if is_free(game_state,attacker["coordX"]+1,attacker["coordY"]+1):
                        return True
    elif (attacker["figureType"] == constants.MORTAR):
        diffX = abs(attacker["coordX"]-defender["coordX"])
        diffY = abs(attacker["coordY"]-defender["coordY"])
        diff = diffX + diffY
        if diff>1 and diff<5:
            if(attacker["coordX"]==defender["coordX"]) or (attacker["coordY"] == defender["coordY"]):
                return True
            elif(diffX == diffY) and diffX > 1 and diffX < 4:
                return True
    elif (attacker["figureType"] == constants.COMMANDO):
        return commando_attack(attacker,defender,game_state)

    return False

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
    att_shift=7
    bait_shift=5
    pos_shift = 5
    setAttacking = set()

    value=0

    for figure in game_state:
        # eval figure
        figure_val=get_figure_value(figure)

        if(figure["playerID"]==on_turn):
            value+=figure_val<<fig_shift

            is_defended=False
            for ally in game_state:
                if ally["playerID"]==on_turn and ally!=figure and is_attacked(ally,figure,game_state):
                    is_defended=True

            for opponent in game_state:
                if opponent["playerID"]!=on_turn and is_attacked(opponent,figure,game_state):
                    if opponent["figureType"]==constants.COMMANDO:
                        if is_defended:
                            value+=figure_val<<bait_shift
                        else:
                            value-=figure_val<<att_shift
                    else:
                        value-=figure_val<<att_shift
        else:
            value-=figure_val

            is_defended=False
            for ally in game_state:
                if ally["playerID"]!=on_turn and ally!=figure and is_attacked(ally,figure,game_state):
                    is_defended=True

            for opponent in game_state:
                if opponent["playerID"]!=on_turn and is_attacked(figure,opponent,game_state):
                    if opponent["figureType"]==constants.COMMANDO:
                        if not is_defended:
                            value+=figure_val<<att_shift
                    else:
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




        



