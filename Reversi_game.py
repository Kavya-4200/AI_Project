"""
Compute the value brought by a given move by placing a new token for player
at (row, column). The value is the number of opponent pieces getting flipped
by the move. 

A move is valid if for the player, the location specified by (row, column) is
(1) empty and (2) will cause some pieces from the other player to flip. The
return value for the function should be the number of pieces hat will be moved.
If the move is not valid, then the value 0 (zero) should be returned. Note
here that row and column both start with index 0. 
"""
import copy
from pprint import pprint
flipped=[]

def get_move_value(state, player, row, column):
    global flipped
    flipped=[]

    if state[row][column]!=' ':
        return 0


    state[row][column]=player
    if player=='B':
        tile='W'
    else:
        tile='B'

    for xdir,ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x,y=row,column
        x+=xdir
        y+=ydir
        if isOnBoard(state,x,y) and state[x][y]==tile:
                x += xdir
                y += ydir
                if not isOnBoard(state,x, y):
                    continue
                while state[x][y] == tile:
                    x += xdir
                    y += ydir

                    if not isOnBoard(state,x, y):  # break out of while loop, then continue in for loop
                             break
                if not isOnBoard(state,x, y):
                    continue

                if state[x][y] == player:
                    while True:
                        x -= xdir
                        y -= ydir
                        if x == row and y == column:
                            break
                        flipped.append([x, y])

    state[row][column]=' '
    if len(flipped)==0:
        return False
    #print(flipped)
    return len(flipped)




"""
Execute a move that updates the state. A new state should be crated. The move
must be valid. Note that the new state should be a clone of the old state and
in particular, should not share memory with the old state. 
"""
def isOnBoard(state,row,column):
    #n=len(state)

    return row >= 0 and row <len(state) and column >= 0 and column <len(state)

def execute_move(state, player, row, column):
    get_move_value(state,player,row,column)
    new_state=flipped

    new_state1 = copy.deepcopy(state)
    if len(new_state)==0:
        return state
    new_state1[row][column]=player
    for x,y in new_state:
        new_state1[x][y]=player

    return new_state1




"""
A method for counting the pieces owned by the two players for a given state. The
return value should be two tuple in the format of (blackpeices, white pieces), e.g.,

    return (4, 3)

"""


def count_pieces(state):
    blackpieces = 0
    whitepieces = 0
    for x in range(len(state)):
        for y in range(len(state)):
            if state[x][y]=='B':
                blackpieces+=1
            elif state[x][y]=='W':
                whitepieces+=1

    return (blackpieces, whitepieces)


"""
Check whether a state is a terminal state. 
"""


def is_terminal_state(state):
   player =['W','B']
   flag=0
   for k in range(len(state)):
           for j in range(len(state)):
               if(state[k][j]!=' '):
                   continue

               if get_move_value(state,player[0],k,j)!=0 or get_move_value(state,player[1],k,j)!=0:
                   flag=1
                   return False

                   break
           '''if flag==1:
               return False'''

   if flag==0:
       return True






   x,y=count_pieces(state)

   if x==0 or y==0 or x+y==(len(state)*len(state)):
       return True
   return False



"""
The minimax algorithm. Your implementation should return the best value for the
given state and player, as well as the next immediate move to take for the player. 
"""
c3=0


def maxi(state, player):
    global c3
    l1 = []
    row = -1
    column = -1

    v1 = -10000
    if is_terminal_state(state):
        c3 += 1
        a, b = count_pieces(state)
        return a - b, [('B', -1, -1)]
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] != ' ':
                continue

            new_state1 = execute_move(state, player, i, j)
            if new_state1 == state:
                continue

            v, s = mini(new_state1, player='W')
            if v > v1:
                v1 = v
                row = i
                column = j
                l1 = s

    if v1 == -10000:
        return mini(state, player='W')

    l1.append(('B', row, column))
    return v1, l1


def mini(state, player):
    l2 = []
    v1 = 10000
    global c3
    if is_terminal_state(state):
        c3 += 1
        a, b = count_pieces(state)
        return a - b, [('W', -1, -1)]
    for i in range(len(state)):
        for j in range(len(state)):
            new_state1 = execute_move(state, player, i, j)
            if state == new_state1:
                continue
            v, s = maxi(new_state1, player='B')
            if v < v1:
                v1 = v
                row = i
                column = j
                l2 = s

    if v1 == 10000:
        return maxi(state, player='B')

    l2.append(('W', row, column))
    return v1, l2


def minimax(state, player):


    if player=='B':
         v,li= maxi(state,player)
         row=li[-1][1]
         column=li[-1][2]
         return v, row,column
    else:
         v,li= mini(state,player)
         row = li[-1][1]
         column = li[-1][2]
         return v, row, column











    # Your implementation goes here
    #return (value, row, column)


"""
This method should call the minimax algorithm to compute an optimal move sequence
that leads to an end game. 
"""


def full_minimax(state, player):
    value = 0
    move_sequence = []
    if player == 'B':
        v, li = maxi(state, player)

        return v, li[::-1]
    else:
        v, li = mini(state, player)

        return v, li[::-1]






"""
The minimax algorithm with alpha-beta pruning. Your implementation should return the
best value for the given state and player, as well as the next immediate move to take
for the player. 
"""

c1=0
c2=0


def max2(state, player, alpha, beta):
    l1 = []
    global c1
    global c2
    row = -1
    column = -1
    v1 = -10000

    if is_terminal_state(state):
        # print("reached here in max?")
        # pprint(state)
        c1 += 1
        a, b = count_pieces(state)
        # print("count",a,b,a-b)
        return a - b, [('B', -1, -1)]
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] != ' ':
                continue

            new_state1 = execute_move(state, player, i, j)
            if new_state1 == state:
                continue

            v, s = min2(new_state1, 'W', alpha, beta)

            if v > v1:
                v1 = v
                row = i
                column = j
                # li.remove(s)
                l1 = s
                # print("list is :",li)

            if v1 >= beta:
                l1.append(('B', row, column))
                c2 += 1
                return v1, l1
            if alpha < v1:
                alpha = v1

    if v1 == -10000:
        # print("come coz max end?")
        # pprint(state)

        return min2(state, 'W', alpha, beta)
        # print("v after maxend",v)
        # l1=s

        # return v,l1
    l1.append(('B', row, column))

    return v1, l1


def min2(state, player, alpha, beta):
    l2 = []

    v1 = 10000
    global c1
    global c2

    if is_terminal_state(state):

        c1 += 1
        a, b = count_pieces(state)
        # print("count",a,b,a-b)
        return a - b, [('W', -1, -1)]
    for i in range(len(state)):
        for j in range(len(state)):
            # print(" i an j ",i,j)
            new_state1 = execute_move(state, player, i, j)
            if state == new_state1:
                continue
            v, s = max2(new_state1, 'B', alpha, beta)

            if v < v1:
                v1 = v
                row = i
                column = j
                # li.remove(s)
                l2 = s
                # print("list is :", li)
            if v1 <= alpha:
                l2.append(('W', row, column))
                c2 += 1
                return v1, l2
            if beta > v1:
                beta = v1

    if v1 == 10000:

        return max2(state, 'B', alpha, beta)

    l2.append(('W', row, column))

    return v1, l2


def minimax_ab(state, player, alpha=-10000000, beta=10000000):
    value = 0
    row = -1
    column = -1

    if player == 'B':
        v, li = max2(state, player,alpha,beta)
        row = li[-1][1]
        column = li[-1][2]
        return v, row, column
    else:
        v, li = min2(state, player,alpha,beta)
        row = li[-1][1]
        column = li[-1][2]
        return v, row, column


#return (value, row, column)


"""
This method should call the minimax_ab algorithm to compute an optimal move sequence
that leads to an end game, using alpha-beta pruning.
"""


def full_minimax_ab(state, player):
    value = 0
    global c1,c2
    move_sequence = []
    if player == 'B':
        v, li = max2(state, player,alpha=-10000000, beta=10000000)
        return v, li[::-1]
    else:
        v, li = min2(state, player,alpha=-10000000, beta=10000000)
        return v, li[::-1]

