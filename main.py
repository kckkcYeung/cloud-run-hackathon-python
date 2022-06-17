import json
import random
import os
import logging
from flask import Flask, request

F = "F"
R = "R"
L = "L"
T = "T"

N = "N"
S = "S"
E = "E"
W = "W"
response = F

NPosition = [W, E, S]
SPosition = [E, W, W]
EPosition = [N, S, W]
WPosition = [S, N, E]

app = Flask(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    httpjson =str(request.get_data().decode("utf-8"))
    print(httpjson)


    j=json.loads(httpjson)
    width=j["arena"]["dims"][0]
    height=j["arena"]["dims"][1]

    w, h = width, height
    board = [[None for y in range(w)] for x in range(h)]

    for key in j["arena"]["state"]:
            x=j["arena"]["state"][key]['x']
            y=j["arena"]["state"][key]['y']
            board[y][x]=key
            if key == j["_links"]["self"]["href"]:
                me = j["arena"]["state"][key]
                
    print(board)
    print(me)
        

    def RandStringRunes(letterRunes) :
            return random.choice(letterRunes)

    
    def checkHasPerson(x, y) :
            if x < 0  or x >= len(board[0]) or y < 0 or y >= len(board) :
                return False
            return board[y][x] != None

    def checkHasPersonInLeft(x, y, direction) :
            if direction == N :
                return checkHasPersonInNextPosition(x, y, NPosition[0])
            elif direction == S:
                return checkHasPersonInNextPosition(x, y, SPosition[0])
            
            elif direction == E:
                return checkHasPersonInNextPosition(x, y, EPosition[0])
            
            elif direction == W:
                return checkHasPersonInNextPosition(x, y, WPosition[0])
            else:
                return False

    def checkHasPersonInRight(x, y, direction) :
            if direction == N :
                return checkHasPersonInNextPosition(x, y, NPosition[1])
            
            elif direction == S:
                return checkHasPersonInNextPosition(x, y, SPosition[1])
            
            elif direction == E:
                return checkHasPersonInNextPosition(x, y, EPosition[1])
            
            elif direction == W:
                return checkHasPersonInNextPosition(x, y, WPosition[1])

            else:
                return False

            
    def checkHasPersonInBack(x, y, direction) :
            if direction == N :
                return checkHasPersonInNextPosition(x, y, NPosition[2])
            elif direction == S:
                return checkHasPersonInNextPosition(x, y, SPosition[2])
            elif direction == E:
                return checkHasPersonInNextPosition(x, y, EPosition[2])
            elif direction == W:
                return checkHasPersonInNextPosition(x, y, WPosition[2])
            else:
                return False


    def checkHasPersonInNextPosition(x, y ,direction) :
            if direction == N:
                return checkHasPerson(x, y-1)
            elif direction == S:
                return checkHasPerson(x, y+1)
            elif direction == E:
                return checkHasPerson(x+1, y)
            elif direction == W:
                return checkHasPerson(x-1, y)
            else:
                return False

    def checkHasPersonInDirection(x, y, direction) :
            if direction == N:
                for i in range(1,4) :
                    if checkHasPerson(x, y-i) :
                        print("checkHasPersonInDirection", x, y-i)
                        return True
                return False
            elif direction == S:
                for i in range(1,4) :
                    if checkHasPerson(x, y+i) :
                        print("checkHasPersonInDirection", x, y+i)
                        return True
                return False
            elif direction == E:
                for i in range(1,4) :
                    if checkHasPerson(x+i, y) :
                        print("checkHasPersonInDirection", x+i, y)
                        return True
                return False
            elif direction == W:
                for i in range(1,4) :
                    if checkHasPerson(x-i, y) :
                        print("checkHasPersonInDirection", x-i, y)
                        return True
                return False
            else:
                return False

    def checkHasPersonInDirection_return_url(x, y, direction) :
            if direction == N:
                for i in range(1,4) :
                    if checkHasPerson(x, y-i) :
                        print("checkHasPersonInDirection", x, y-i)
                        return board[y-i][x]
    
            elif direction == S:
                for i in range(1,4) :
                    if checkHasPerson(x, y+i) :
                        print("checkHasPersonInDirection", x, y+i)
                        return board[y+i][x]
                
            elif direction == E:
                for i in range(1,4) :
                    if checkHasPerson(x+i, y) :
                        print("checkHasPersonInDirection", x+i, y)
                        return board[y][x+i]
                
            elif direction == W:
                for i in range(1,4) :
                    if checkHasPerson(x-i, y) :
                        print("checkHasPersonInDirection", x-i, y)
                        return board[y][x-i]




            
    def isBuilding(x, y, direction ) :
            if direction == N:
                return y == 0
            elif direction == S:
                return y == len(board)-1
            elif direction == E:
                return x == len(board[0])-1
            elif direction == W:
                return x == 0
            else:
                return False

    def finddatafromurl(url):
        data = j["arena"]["state"][url]
        return data

    


            
            
    if me["wasHit"] ==  True:
         if isBuilding(me["x"], me["y"], me["direction"] ):
                print("is builing")
                response = RandStringRunes("RL")
                if response == R:
                    if me["direction"] == N:
                        predir = E
                    if me["direction"] == S:
                        predir = W
                    if me["direction"] == E:
                        predir = S
                    if me["direction"] == W:
                        predir = N
                        
                    if isBuilding(me["x"], me["y"], predir ):
                        response = L

                if response == L:
                    if me["direction"] == N:
                        predir = W
                    if me["direction"] == S:
                        predir = E
                    if me["direction"] == E:
                        predir = N
                    if me["direction"] == W:
                        predir = S
                    if isBuilding(me["x"], me["y"], predir ):
                        response = R
         else:
                try:
                    attacker = checkHasPersonInDirection_return_url(me["x"],me["y"],me["direction"])

                except :
                    attacker = j["_links"]["self"]["href"]
                if attacker != "":
                    try :
                        attacker_direction = finddatafromurl(attacker)["direction"]

                    except:
                        attacker_direction = RandStringRunes("NSEW")

                    if attacker_direction == "N":
                        if me["direction"] == "S":
                            response =  RandStringRunes("RL")
                        else :
                            response = T

                    if attacker_direction == "S":
                        if me["direction"] == "N":
                            response =  RandStringRunes("RL")
                        else :
                            response = T

                    if attacker_direction == "E":
                        if me["direction"] == "W":
                            response =  RandStringRunes("RL")
                        else :
                            response = T

                    if attacker_direction == "W":
                        if me["direction"] == "E":
                            response =  RandStringRunes("RL")
                        else :
                            response = T
                    else:
                        response = RandStringRunes("FFRL")
                            

                    
                    
        
    elif checkHasPersonInDirection(me["x"], me["y"], me["direction"]) :
            print("Has person In Direction")
            response = T
    elif checkHasPersonInRight(me["x"], me["y"], me["direction"]):
            print("Has person In Right")
            response = R
    elif checkHasPersonInLeft(me["x"], me["y"], me["direction"]):
            print("Has person In Left")
            response = L
    else :
            if isBuilding(me["x"], me["y"], me["direction"] ):
                print("is builing")
                response = RandStringRunes("RL")
                if response == R:
                    if me["direction"] == N:
                        predir = E
                    if me["direction"] == S:
                        predir = W
                    if me["direction"] == E:
                        predir = S
                    if me["direction"] == W:
                        predir = N
                        
                    if isBuilding(me["x"], me["y"], predir ):
                        response = L

                if response == L:
                    if me["direction"] == N:
                        predir = W
                    if me["direction"] == S:
                        predir = E
                    if me["direction"] == E:
                        predir = N
                    if me["direction"] == W:
                        predir = S
                    if isBuilding(me["x"], me["y"], predir ):
                        response = R

                    
            else:
                acount=0
                for i in range(int(width/2)):
                    for j in range(int(height/2)):
                        if checkHasPerson(i,j):
                            acount = acount + 1
                            
                bcount=0
                for i in range(int(width/2), int(width)):
                    for j in range(int(height/2)):
                        if checkHasPerson(i,j):
                            bcount = bcount + 1

                ccount=0
                for i in range(int(width/2)):
                    for j in range(int(height/2), int(height)):
                        if checkHasPerson(i,j):
                            ccount = ccount + 1

                dcount=0
                for i in range(int(width/2),int(width)):
                    for j in range(int(height/2),int(height)):
                        if checkHasPerson(i,j):
                            dcount = dcount + 1

                print(acount)
                print(bcount)
                print(ccount)
                print(dcount)
                
                finalcount = "acount"
                if acount > bcount and acount > ccount and acount > dcount :
                    finalcount = "a"
    
                
                if bcount > acount and bcount > ccount and bcount > dcount :
                    finalcount = "b"
                
                
                if ccount > acount and ccount > bcount and ccount > dcount :
                    finalcount = "c"
                
                
                if dcount > acount and dcount > bcount and dcount > ccount :
                    finalcount = "d"
                
                megroup = "a"
                if me["x"] < int(width/2) and me["y"] < int(height/2):
    
                    megroup = "a"
                
                
                if me["x"] >= int(width/2) and me["y"] < int(height/2):
                
                    megroup = "b"
                
                
                
                if me["x"] < int(width/2) and me["y"] >= int(height/2):
       
                    megroup = "c"
                
                
                if me["x"] >= int(width/2) and me["y"] >= int(height/2):
                    megroup = "d"

                print(finalcount)
                print(megroup)
                if megroup == finalcount:
                    response = RandStringRunes("FFRL")
                else:
                    if megroup == "a":
                           if finalcount == "b" :
                               if me["direction"] == N:
                                   response = R
                               if me["direction"] == S:
                                   response = L
                               if me["direction"] == E:
                                   response = F
                               if me["direction"] == W:
                                   response = L
                           if finalcount == "c" :
                               if me["direction"] == N:
                                   response = L
                               if me["direction"] == S:
                                   response = F
                               if me["direction"] == E:
                                   response = R
                               if me["direction"] == W:
                                   response = L
                           if finalcount == "d" :
                               if me["direction"] == N:
                                   response = R
                               if me["direction"] == S:
                                   response = F
                               if me["direction"] == E:
                                   response = F  
                               if me["direction"] == W:
                                   response = L
                                   
                    if megroup == "b":
                            if finalcount == "a" :
                                if me["direction"] == N:
                                    response = L
                                if me["direction"] == S:
                                    response = R
                                if me["direction"] == E:
                                    response = R
                                if me["direction"] == W:
                                    response = F
                            if finalcount == "c" :
                                if me["direction"] == N:
                                    response = L 
                                if me["direction"] == S:
                                    response = F
                                if me["direction"] == E:
                                    response = R
                                if me["direction"] == W:
                                    response = F
                            if finalcount == "d" :
                                if me["direction"] == N:
                                    response = L
                                if me["direction"] == S:
                                    response = F
                                if me["direction"] == E:
                                    response = R
                                if me["direction"] == W:
                                    response = L

                    if megroup == "c":
                            if finalcount == "a" :
                                if me["direction"] == N:
                                    response = F
                                if me["direction"] == S:
                                    response = L
                                if me["direction"] == E:
                                    response = L
                                if me["direction"] == W:
                                    response = R
                            if finalcount == "b" :
                                if me["direction"] == N:
                                    response = F
                                if me["direction"] == S:
                                    response = L
                                if me["direction"] == E:
                                    response = F
                                if me["direction"] == W:
                                    response = R
                            if finalcount == "d" :
                                if me["direction"] == N:
                                    response = R
                                if me["direction"] == S:
                                    response = L
                                if me["direction"] == E:
                                    response = F
                                if me["direction"] == W:
                                    response = R
                    if megroup == "d":
                            if finalcount == "a" :
                                if me["direction"] == N:
                                    response = F
                                if me["direction"] == S:
                                    response = R
                                if me["direction"] == E:
                                    response = L
                                if me["direction"] == W:
                                    response = F
                            if finalcount == "b" :
                                if me["direction"] == N:
                                    response = F
                                if me["direction"] == S:
                                    response = R
                                if me["direction"] == E:
                                    response = L
                                if me["direction"] == W:
                                    response = R
                            if finalcount == "c" :
                                if me["direction"] == N:
                                    response = L
                                if me["direction"] == S:
                                    response = R
                                if me["direction"] == E:
                                    response = L
                                if me["direction"] == W:
                                    response = F

            
    return response




        




if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
