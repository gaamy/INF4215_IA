# Tile problem
#
# Author: Michel Gagnon
#         michel.gagnon@polytml.ca
#
# The problem consists in a grid that should be covered by tiles.
# Some squares in the grid are obstacles that cannot be covered by a tile
# Three types of tile can be used: a single square, a 2X2 square, or a rectangle
# that covers two adjacent squares.
# We must cover the grid by minimizing the number of tiles

from node import *
from state import *
from breadthfirst_search import *
from depthfirst_search import *
from astar_search import *


class TileState(State):
    def __init__(self,(dimX,dimY),obstacles):
        self.dimensions = (dimX,dimY)
        self.obstacles = obstacles
        self.grid = self._createGrid(dimX,dimY,obstacles)
        self.counter = 0
        self.emptyCells = dimX*dimY - len(obstacles)

    def equals(self,state):
        return self.grid == state.grid

    def show(self):
        for row in self.grid:
            for cell in row:
                if cell == -1:
                    print '**',
                else:
                    print '{:2}'.format(cell),
            print

    def executeAction(self,(action,x,y)):
        self.counter += 1
        if action == 'addSmallSquare':
            self.grid[x][y] = self.counter
            self.emptyCells -= 1
        elif action == 'addBigSquare':
            self.grid[x][y] = self.counter
            self.grid[x+1][y] = self.counter
            self.grid[x][y+1] = self.counter
            self.grid[x+1][y+1] = self.counter
            self.emptyCells -= 4
        elif action == 'addHorizontalRectangle':
            self.grid[x][y] = self.counter
            self.grid[x][y+1] = self.counter
            self.emptyCells -= 2
        elif action == 'addVerticalRectangle':
            self.grid[x][y] = self.counter
            self.grid[x+1][y] = self.counter
            self.emptyCells -= 2
        else:
            raise Exception('Erreur')

    def possibleActions(self):
        actions = []
        (dimX,dimY) = self.dimensions
        for i in range(dimX):
            for j in range(dimY):
                if self.grid[i][j] == 0:
                    actions.append(('addSmallSquare',i,j))
                    if j < dimY-1 and self.grid[i][j+1] == 0:
                        actions.append(('addHorizontalRectangle',i,j))
                    if i < dimX-1 and self.grid[i+1][j] == 0:
                        actions.append(('addVerticalRectangle',i,j))
                    if i < dimX-1 and j < dimY-1 and self.grid[i][j+1] == 0 and self.grid[i+1][j] == 0 and self.grid[i+1][j+1] == 0:
                        actions.append(('addBigSquare',i,j))
        return actions

    def cost(self,action):
        return 1

    def isGoal(self):
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    return False
        return True


    def heuristic(self):
        a = self.emptyCells / 4
        b = self.emptyCells % 4
        if b == 0:
            return a
        elif b == 3:
            return a+2
        else:
            return a+1

    ### Private methods ####

    def _createGrid(self,dimX,dimY,obstacles):
        grid = [ [0 for y in range(dimY)] for x in range(dimX) ]
        for i in range(dimX):
            for j in range(dimY):
                if (i,j) in obstacles:
                    grid[i][j] = -1
        return grid



solution = astar_search(TileState((3,4),[(1,2)]))

