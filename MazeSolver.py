import os
import math
from simpleai.search import astar, SearchProblem
#execute :  pip install simpleai @ the terminal

class MazeSolver(SearchProblem):
    def __init__(self, src_board):
        #loading the maze board in memory
        if not os.path.exists(src_board):
            raise Exception(src_board + ' doesnt exist!')

        #board (adj matrix)
        self.board = []

        #open the file (source for board)
        f_handle = open(src_board, 'r')
        for x in f_handle:
            x = x.strip() #remove the leading/trailing spaces and newline
            self.board.append([y for y in x])
        f_handle.close()

        #Recording the positions of turtle and the egg
        self.initial_pos = None
        self.goal_pos = None

        for i in range (len(self.board)):
            for j in range (len(self.board[i])):
                if self.board[i][j] == 'x': #turtle
                    self.initial_pos = (i,j)
                if self.board[i][j] == 'o':  # egg
                    self.goal_pos = (i,j)

        if self.initial_pos is None:
            raise Exception('Turtle not found')

        if self.goal_pos is None:
            raise Exception('Egg not found')

        #Define the costs
        regular_cost = 1
        diagonal_cost = 1.7

        self.COSTS = {
            "UP": regular_cost,
            "DOWN" : regular_cost,
            "LEFT" : regular_cost,
            "RIGHT" : regular_cost,
            "UP LEFT" : diagonal_cost,
            "UP RIGHT": diagonal_cost,
            "DOWN LEFT": diagonal_cost,
            "DOWN RIGHT" : diagonal_cost
        }

        #initial the super class sub object
        SearchProblem.__init__(self,initial_state = self.initial_pos)

    #This method receives a state and must return a list of actions that can be taken ahead
    def actions(self, state):
        possible_moves = []
        for amove in self.COSTS.keys():
            newx, newy = self.result(state, amove)
            if self.board[newx][newy] != '#':
                possible_moves.append(amove)

        return possible_moves

    #This method receives current state (coordinates) and an action (a move)
    #It must return a new state (coordinates) that results by application of the action (a move)
    def result(self, state, action):
        x,y = state #coordinates
        if action.count('UP'):
            y-=1
        if action.count('DOWN'):
            y+=1
        if action.count('LEFT'):
            x-=1
        if action.count('RIGHT'):
            x+=1
        return x,y #new state

    def display_board(self):
        for x in self.board:
            print()
            for y in x:
                print(y, end='')

    #This method helps A* control the iterations
    def is_goal(self, state):
        return  state == self.goal_pos

    #This method returns the h value (estimated cost) to reach the goal given the current state
    def heuristic(self, state):
        #euclidean distance
        x1,y1 = state
        x2,y2 = self.goal_pos
        p1 = (x1-x2) **2
        p2 = (y1-y2) **2
        estimated_cost = math.sqrt(p1+p2)
        return estimated_cost

    #This method returns the cost wrt a move
    def cost(self, state, action, state2):
        return self.COSTS[action]

    def solve(self):
        result = astar(self, graph_search=True)
        #graph_search = True, A* avoids exploring the repeated states
        path_to_goal = result.path()

        #delete the first and last element of path_to_goal
        path_to_goal.pop(0) #turtle position
        path_to_goal.pop(-1) #egg position

        #draw the breadcrums
        for _,pos in path_to_goal:
            self.board[pos[0]][pos[1]]= '.'

        self.display_board()

#use any text files provided
def main():
    ms = MazeSolver('C:/Users/hp/OneDrive/Desktop/Python Projects/MazeSolver/maze_boards/4.txt') #path of the txt file
    ms.solve()

main()



