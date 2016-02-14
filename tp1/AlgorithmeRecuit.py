__author__ = 'frrivd'

from node import *
from state import *
from beam_search import *
import time
import random

from node import *
from state import *
import time
import random

from simulated_annealing import *

class AlgorithmeRecuit(State):
    def __init__(self,positionDesAntennes):
        self.positionDesAntennes = positionDesAntennes
        self.vars = [random.randint(0,dim-1) for i in range(dim)]
        self.constraints = []
        for i in range(dim):
            for j in range(i+1,dim):
                self.constraints.append(([i,j],'self.vars[{0}] != self.vars[{1}]'.format(i,j)))
                self.constraints.append(([i,j],'self.vars[{0}] + {1} != self.vars[{2}]'.format(i,j-i,j)))
                self.constraints.append(([i,j],'self.vars[{0}] - {1} != self.vars[{2}]'.format(i,j-i,j)))

    def equals(self,state):
        return self.vars == state.vars

    def show(self):
        print self.vars

    def executeAction(self,(i,val)):
        self.vars[i] = val

    def possibleActions(self):
        # Randomly select a variable
        # v = random.randint(0,self.dim - 1)

        # Select a variable thas is involved in one contraint at least
        violatingVars = set([v for (scope,c) in self.constraints if not eval(c) for v in scope])
        v = random.choice(list(violatingVars))
        possibleValues = range(self.dim)
        possibleValues.remove(self.vars[v])
        return [(v, random.choice(possibleValues))]

    def cost(self,action):
        return 1

    def isGoal(self):
        return self.consistent()

    def heuristic(self):
        return sum([1 if not eval(c) else 0 for (scope,c) in self.constraints])

    def consistent(self):
        return all([eval(c) for (scope,c) in self.constraints])



start = time.time()
positionDesAntennes = ([(30,0),(10,10),(20,20),(30,40),(50,40)],200,1)
q = AlgorithmeRecuit(positionDesAntennes)
while simulated_annealing_search(q,0.1,0.01,100) == None:
    print "Restart..."
    q = AlgorithmeRecuit(positionDesAntennes)
end = time.time()
print '{} seconds'.format(end-start)



#search([(30,0),(10,10),(20,20),(30,40),(50,40)],200,1)
