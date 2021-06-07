import random
from random import randrange
from copy import deepcopy
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For Search Algorithms 
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''

'''
BFS add to queue 
'''
#import queue as q
from collections import deque
import queue as q

queue2 = q.Queue()
#expansions = 0
def add_to_queue_BFS(node_id, parent_node_id, cost, initialize=False):
    global queue2
    if initialize:
        queue2 = q.Queue()

    if queue2 is not None:
        queue2.put((node_id, parent_node_id))

    return

'''
BFS add to queue 
'''
def is_queue_empty_BFS():
    global queue2
    if queue2.qsize()==0:
        return True
    # Your code here
    return False

'''
BFS pop from queue
'''
def pop_front_BFS():

    return queue2.get()

'''
DFS add to queue 
'''

queue1=[]
#queue1=q.LifoQueue()
def add_to_queue_DFS(node_id, parent_node_id, cost, initialize=False):
    # Your code here
    global queue1
    if initialize:
        #queue1=[]
        queue1=[]

    if queue1 is not None:
        queue1.append((node_id,parent_node_id))
        #queue1.append((node_id,parent_node_id))


    return

'''
DFS add to queue 
'''
def is_queue_empty_DFS():
    global queue1

    if len(queue1)==0:
        return True
    # Your code here
    return False

'''
DFS pop from queue
'''
def pop_front_DFS():
    #(node_id, parent_node_id) = (0, 0)
    # Your code here
    return queue1.pop()

'''
UC add to queue 
'''

#from queue import PriorityQueue
from queue import PriorityQueue
queue3= PriorityQueue()
def add_to_queue_UC(node_id, parent_node_id, cost, initialize=False):
    # Your code here
    global queue3
    if initialize:
        queue3=PriorityQueue()
    if queue3 is not None:
        queue3.put((cost,node_id,parent_node_id))
    return

'''
UC add to queue 
'''
def is_queue_empty_UC():
    # Your code here
    global queue3
    if queue3 is None:
        return True
    return False

'''
UC pop from queue
'''
def pop_front_UC():
    #(node_id, parent_node_id) = (0, 0)
    # Your code here
    global queue3
    if queue3 is None:
        return (None,None)

    return queue3.get()[1:]


'''
A* add to queue 
'''
queue4=PriorityQueue()
def add_to_queue_ASTAR(node_id, parent_node_id, cost, initialize=False):
    global queue4
    if initialize:
        queue4=PriorityQueue()
    if queue4 is not None:
        queue4.put((cost,node_id,parent_node_id))
    # Your code here
    return

'''
A* add to queue 
'''
def is_queue_empty_ASTAR():
    global queue4
    # Your code here

    if queue4 is None:
        return True
    return False


'''
A* pop from queue
'''
def pop_front_ASTAR():
    global queue3
    if queue3 is None:
        return (None, None)
    # Your code here
    return queue4.get()[1:]

''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For n-queens problem 
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''



#Compute a random state

def get_random_state(n):
    state = []
    side_length=n
    open_columns = list(range(side_length))
    queen_num=n

    i=0
    queen_positions=[]

    for _ in range(queen_num):
        queen_positions.append(randrange(1,side_length+1))


    return queen_positions


'''
#Compute pairs of queens in conflict
'''


def compute_attacking_pairs(queen_positions):

        for i in range(len(queen_positions)):
            queen_positions[i]=[queen_positions[i],i]

        def range_between(a, b):
            if a > b:
                return range(a - 1, b, -1)
            elif a < b:
                return range(a + 1, b)
            else:
                return [a]

        def zip_repeat(a, b):
            if len(a) == 1:
                a = a * len(b)
            elif len(b) == 1:
                b = b * len(a)
            return zip(a, b)

        # Finds all the points in between two points
        def points_between(a, b):
            return zip_repeat(list(range_between(a[0], b[0])), list(range_between(a[1], b[1])))


        def is_attacking(queens, a, b):
            if (a[0] == b[0]) or (a[1] == b[1]) or (abs(a[0] - b[0]) == abs(a[1] - b[1])):
                for between in points_between(a, b):
                    if between in queens:
                        return False
                return True
            else:
                return False

        attacking_pairs = []
        queen_positions = list(queen_positions)
        left_to_check = deepcopy(queen_positions)
        while left_to_check:
            a = left_to_check.pop()
            for b in left_to_check:
                if is_attacking(queen_positions, a, b):
                    attacking_pairs.append([a, b])


        return len(attacking_pairs)


'''
#The basic hill-climing algorithm for n queens
'''
import copy

def hill_descending_n_queens(queen_positions,compute_attacking_pairs):


    min=compute_attacking_pairs(queen_positions)

    final_state=copy.deepcopy(queen_positions)

    for i in range(len(queen_positions)):
        queen_positions[i] = queen_positions[i][0]




    for i in range(len(queen_positions)):
        j=1
        l = queen_positions[i]
        while j<len(queen_positions):

            queen_positions[i]=j


            attack=compute_attacking_pairs(queen_positions)

            if attack<min:
                min=attack
                final_state=copy.deepcopy(queen_positions)

            j+=1

            for k in range(len(queen_positions)):
                queen_positions[k] = queen_positions[k][0]

        queen_positions[i]=l


    for k in range(len(final_state)):
        final_state[k]=final_state[k][0]

    return final_state


'''
#Hill-climing algorithm for n queens with restart
'''
def n_queens(n, get_random_state, compute_attacking_pairs, hill_descending_n_queens):
    queen_positions = get_random_state(n)
    while True:

            fs=hill_descending_n_queens(queen_positions,compute_attacking_pairs)

            if fs == queen_positions:
                queen_positions = get_random_state(n)
                continue

            elif compute_attacking_pairs(fs)!=0:
                queen_positions = fs
                queen_positions = [queen_positions[i][0] for i in range(len(queen_positions))]

                continue


            else:
                for i in range(len(fs)):
                    fs[i]=fs[i][0]
                return fs


















