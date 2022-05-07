
def isFree(game_state:dict,x:int,y:int):
    for figure in game_state:
        if(figure["coordX"]==x and figure["coordY"]==y):
            return True
    return False

def isAttacked(attacker:dict, defender:dict, game_state:list):

    #Infantry
    if (attacker["figureType"] == 0):

        #ista x koordinata
        if(attacker["coordX"]==defender["coordX"]):
            if(abs(attacker["coordY"]-defender["coordY"])==1):
                return True
            elif(attacker["coordY"]-defender["coordY"]==2 and isFree(game_state,attacker["coordX"],attacker["coordY"]-1)):
                return True
            elif(attacker["coordY"] - defender["coordY"] == -2 and isFree(game_state,attacker["coordX"],attacker["coordY"]+1)):
                return True

        #ista y koordinata
        if (attacker["coordY"] == defender["coordY"]):
            if (abs(attacker["coordX"] - defender["coordX"]) == 1):
                return True
            elif (attacker["coordX"] - defender["coordX"] == 2 and isFree(game_state, attacker["coordX"]-1,attacker["coordY"])):
                return True
            elif (attacker["coordX"] - defender["coordX"] == -2 and isFree(game_state, attacker["coordX"]+1,attacker["coordY"])):
                return True

    #Gunner
    elif (attacker["figureType"] == 1):
        diff=(abs(attacker["coordY"]-defender["coordY"])+abs(attacker["coordX"]-defender["coordX"]))
        if diff==2 or diff==3:
            #u opsegu za napad, provera za izmedju
    elif (attacker["figureType"] == 2):
        figure_val = 1500
    elif (attacker["figureType"] == 3):
        figure_val = 2000

def evaluate(game_state:list,on_turn:str):
    value=0

    for figure in game_state:
        # eval figure
        figure_val=0
        if(figure["figureType"]==0):
            figure_val=1000
        elif(figure["figureType"]==1):
            figure_val=1250
        elif (figure["figureType"] == 2):
            figure_val=1500
        elif (figure["figureType"] == 3):
            figure_val=2000
        if(figure["playerID"]==on_turn):
            value+=figure_val


        else:
            value-=figure_val



