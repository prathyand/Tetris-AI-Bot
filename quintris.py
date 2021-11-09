from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
import copy
import inspect
from multiprocessing import Pool
class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the heuristic function that returns a heuristic value for given input board
# 
def heur(brd):
    hr=0 
    brd2=copy.copy(brd)
    for i in range(len(brd2)):
        brd2[i]=[0 if x==' ' else x for x in list(brd2[i])] #fill empty space with 0
    for i in range(len(brd)):          
        for j in range(len(brd[0])):
            if(brd[i][j]=='x'):
                continue
            if(i!=0):
                if([foo[j] for foo in brd2[0:i]].count('x')>0):#If the given position is bloacked from above
                    hr+=(len(brd)-i+2)**4 # increase hr by (height of the position +2)**4
            if(j!=0):
                if(brd[i][j-1]=='x'):#If the given position is bloacked from left side
                    hr+=(len(brd)-i+2)**2 #increase hr by (height of the position +2)**2
            if(j!=len(brd[0])-1):
                if(brd[i][j+1]=='x'):#If the given position is bloacked from right side
                    hr+=(len(brd)-i+2)**2 #increase hr by (height of the position +2)**2
    return hr


#####
# This function returns the lowest heuristic value among all successors of input board
# 
def minsucc(quintris):
    brd=quintris.get_board()
    rw,cl=len(brd),len(brd[0])
    visited=set() #set to keep track of already explored successors
    hrmin=10000000 #initiate global min with +inf
    best_board=None
    c=quintris.col
    for j in range(-c,cl-c):#for loop to loop through lateral movements of the piece
        cpy1=copy.copy(quintris)
        mv=""
        if(j<0):
            for k in range(1,-j+1):
                mv+="b"
                cpy1.left()      
        elif(j>0):
            for k in range(1,j+1):
                cpy1.right()
                mv+="m"
        for i in range (1,5):#for loop to loop through rotations of the piece by 90,180,270,360 degrees
            cpy2=copy.copy(cpy1) 
            for k in range(1,i+1):
                cpy2.rotate()
            mv2=mv+(i%4)*"n"
            cpy3=copy.copy(cpy2)
            try:
                cpy2.down()
                brd1=cpy2.get_board()
                if(tuple(brd1) not in visited):
                    cm=heur(brd1)
                    if(hrmin>cm):#if lower value found,update the global min
                        best_board=brd1
                        hrmin=cm
                    visited.add(tuple(brd1))
            except EndOfGame as s:
                pass
            cpy3.hflip()#flip the piece and check the heuristic
            mv2=mv2+"h"
            try:
                cpy3.down()
                brd2=cpy3.get_board()
                if(tuple(brd2) not in visited):
                    cm=heur(brd2)
                    if(hrmin>cm):#if lower value found,update the global min
                        best_board=brd2
                        hrmin=cm
                    visited.add(tuple(brd2))
            except EndOfGame as s:
                continue  
    return (hrmin,best_board) #return best board config and min heuristic value

#
#This function generates all possible successors of the given input board and passes those successors to 'minsucc()' 
#to find the minimum heuristic move for all possible moves of 'next_piece'. It ruturns the best move 
# as a string
#
def successor0(quintris):
    brd=quintris.get_board()
    rw,cl=len(brd),len(brd[0])
    visited=set()
    mymin=1000000000 #initiate min to +inf
    best_move=None
    best_board=None
    bestbrd2=None
    c=quintris.col
    A=[] #List to hold all possible unique successors of input board
    mvs=[]
    brds=[]
    for j in range(-c,cl-c):#for loop to loop through lateral movements of the piece
        cpy1=copy.copy(quintris)
        mv=""
        if(j<0):
            for k in range(1,-j+1):
                mv+="b"
                cpy1.left()      
        elif(j>0):
            for k in range(1,j+1):
                cpy1.right()
                mv+="m"
        for i in range (1,5):#for loop to loop through rotations of the piece by 90,180,270,360 degrees
            cpy2=copy.copy(cpy1) 
            for k in range(1,i+1):
                cpy2.rotate()
            mv2=mv+(i%4)*"n"
            cpy3=copy.copy(cpy2)
            try:
                cpy2.down()
                brd1=cpy2.get_board()
                if(tuple(brd1) not in visited):
                    A.append(cpy2) #if unique successor found, add it to the list
                    mvs.append(mv2)
                    visited.add(tuple(brd1))
                else:
                    pass
            except EndOfGame as s:
                pass
            cpy3.hflip()#flip the current piece
            mv2=mv2+"h"
            try:
                cpy3.down()
                brd2=cpy3.get_board()
                if(tuple(brd2) not in visited):
                    A.append(cpy3)#if unique successor found, add it to the list
                    mvs.append(mv2)
                    visited.add(tuple(brd2))
                else:
                    pass
            except EndOfGame as s:
                continue
    with Pool(processes=12) as pool: #create a pool object to use multiprocessing for faster computation
        resultss=pool.map(minsucc,A)
    pool.close()
    pool.join()
    outputs = [result[0] for result in resultss]
    cm=min(outputs)
    mind=outputs.index(cm)
    mymin=cm
    best_move=mvs[mind]
    return (best_move,mymin) #return the move with lowest heuristic considering current piece and next piece
    
    
class ComputerPlayer:
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        mymove=successor0(quintris)[0]
        return mymove

    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            mymove=successor0(quintris)[0]
            bs=mymove.count('b')
            ns=mymove.count('n')
            ms=mymove.count('m')
            hs=mymove.count('h')
            for i in range(bs):
                quintris.left()
            for i in range(ms):
                quintris.right()
            for i in range(ns):
                quintris.rotate()
            for i in range(hs):
                quintris.hflip()
            quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



