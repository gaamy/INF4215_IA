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

# TP1 Couverture des antennes, version arboressante
#
# Author: Gabriel Amyot & Francis Rivest
#

from node import *
from state import *
import matplotlib.pyplot as plt
from antenna import *
from point import *
from astar_search import *

import math

class AlgorithmeRecuitState(State):


    threshold = 1000

    def __init__(self,coordinateList,K,C):
        self.K = K
        self.C = C
        self.counter = 0
        self.antennaList = []
        self.pointList = []
        for (x,y) in coordinateList:
			self.pointList.append(Point(x,y))

        self.smallDistance = self._defineSmallDistance_()



    # Checks whether current state and the one passed as parameter are exactly the same
    def equals(self,state):
        #TODO: I dont know if a list of objects can be compared like that
        return self.antennaList == state.antennaList


    # Checks whether the state is a goal state
    # the goal of this algorithm is to optimise the coverage of all points,
    # but we'll never have a way to know for sure if we got schwifty
    # The alternative is to stop searching after a predetermined amount of
    # actions verifying if we covered all the points
    def isGoal(self):
        coveredPoints = self.coveredPoints()
        if coveredPoints:
            if len(coveredPoints) == len(self.pointList):
                self.optimise(coveredPoints)
                return True
        return False


    def optimise(self,coveredPoints):
        coveredPoints

    # Prints to the console a description of the state
    def show(self):

        #print("Covered points:  %s  " % (len(list(set(self.pointList)-set(self.uncoveredPoints())))))

        print ("Remaining points to cover:  %s "  %(len(self.uncoveredPoints())))
        print ("Cost remaining to reach the target:  h(n)= %s" %(self.heuristic()))
        print ("Cost to reach the current state: g(n)= %s" %(self.g()))
        print ("Total cost:  f(n)=%s" %(self.f()))
        print ("#Steps=  %s" %(self.counter))

        print 'Placed antennas:'
        if self.antennaList != None:
            for antenna in self.antennaList:
                print("---Antenna# %s position=(%s,%s) r= %s"
                      %(self.antennaList.index(antenna),
                        antenna.position.x,
                        antenna.position.y,
                        antenna.radius)
                      )

        #plt.plot()


    # Returns a list of possible actions with the current state
    def possibleActions(self):
        uncoveredPoints = self.uncoveredPoints()
        actionList = []

        #action 1 : ajouter antenne sur 1 point
        point = random.choice(uncoveredPoints)
        actionList.append(('addSimpleAntenna',point))

        #action 2: antenne entre les 2 point les plus proches non couverts

        pt1 = random.choice(uncoveredPoints)
        pt2 = random.choice(uncoveredPoints)
        if pt1 != pt2 :
           actionList.append(('addAntennaBetween2',pt1,pt2))


        #action 3
        if len(self.antennaList) > 0:
            antenna = random.choice(self.antennaList)
            if antenna.affectedPoints:
                actionList.append(('growAntenna',antenna.position))

        return actionList

     # State is changed according to action
    #Params:  (actionName,pointList)
    def executeAction(self,action):
        self.counter += 1
        actionName = action[0]
        if actionName == 'addSimpleAntenna':
            newPoint = action[1]
            newAntenna = Antenna()
            newAntenna.addPoint(newPoint)
            self.antennaList.append(newAntenna)
        elif actionName == 'addAntennaBetween2':
            newPoint1 = action[1]
            newPoint2 = action[2]
            newAntenna = Antenna()
            newAntenna.addPointList([newPoint1,newPoint2])
            self.antennaList.append(newAntenna)
        elif actionName == 'growAntenna':
            antennaPosition = action[1]
            nearestPoint = self._nearestFrom_(antennaPosition, self.uncoveredPoints())
            if nearestPoint != None:
                antenna = self._antennaAt_(antennaPosition)
                antenna.addPoint(nearestPoint)
        #elif actionName == 'shrinkAntenna':
            #oldAntennaPosition = action[1]
            #oldAntenna = self._antennaAt_(oldAntennaPosition)
            #oldAntenna.shrink()
        else:
            raise Exception('Erreur')

    # Returns the cost of executing some action
    # By default, we suppose that all actions have the same cost = 1
    # action >> (actionName,pointList)
    """
    def cost(self,action):
        self.counter += 1
        #calculate current cost _g_()
        baseCost = self.g()
        #make a copy of the current state
        newState = copy.deepcopy(self)
        #apply the action changes on the copyed state
        actionName = action[0]
        if actionName == 'addSimpleAntenna':
            newPoint = action[1]
            self.antennaList.append(Antenna().addPoint(newPoint))
        elif actionName == 'addAntennaBetween2':
            newPoint1 = action[1]
            newPoint2 = action[2]
            self.antennaList.append(Antenna().addPointList([newPoint1,newPoint2]))
        elif actionName == 'growAntenna':
            antennaPosition = action[1]
            nearestPoint = self._nearestFrom_(antennaPosition, self.uncoveredPoints())
            antenna = self._antennaAt_(antennaPosition)
            antenna.addPoint(nearestPoint)
        elif actionName == 'shrinkAntenna':
            oldAntennaPosition = action[1]
            oldAntenna = self._antennaAt_(oldAntennaPosition)
            oldAntenna.shrink()

        #calculates _g_() for the modified state
        newCost = newState.g()

        return newCost - baseCost
    """


    # Returns a heuristic value that provides an estimate of the remaining
    # cost to achieve the goal. By default, value is 0
    def heuristic(self):
        if self.coveredPoints() != None:
            amountOfRemainingPoints = len(self.pointList) - len(self.coveredPoints())
            return amountOfRemainingPoints * self.K
        else:
            return len(self.pointList)*self.K


     ### Private methods ####
    # g(n) represents the exact cost of the path from the starting point
    # to any vertex n
    def g(self):
        cost = 0
        if self.antennaList:
            for antenna in self.antennaList:
                cost += self.K + self.C * antenna.radius**2
        return cost

    def f(self):
        return self.g() + self.heuristic()

    #M(A,B)
    #Return the distance between 2 points
    def distanceBetween(self,pt1,pt2):
        return math.sqrt( (pt2.x-pt1.x)**2 + (pt2.y-pt1.y)**2 )

    # return 2 point that are the closest in the list
    def _closestPoints_(self, pointsList):
        pointA = pointsList[0]
        pointB = pointsList[1]
        for point1 in pointsList:
            for point2 in pointsList:
                if point1 != point2 and  self.distanceBetween(point1, point2) < self.distanceBetween(pointA, pointB):
                    pointA = point1
                    pointB = point2
        return (pointA,pointB)

    #return the less distant point from referencePoint in pointList
    def _nearestFrom_(self,referencePoint,pointList):
        if pointList:
            pointA = pointList.pop()
            for point1 in pointList:
                if point1 != referencePoint and self.distanceBetween(point1, referencePoint) < self.distanceBetween(pointA, referencePoint):
                    pointA = point1
            return pointA
        else:
            return None

    def uncoveredPoints(self):
        if self.coveredPoints() == None:
            return self.pointList
        else:
           # l = self.coveredPoints()
            return list(set(self.pointList) - set(self.coveredPoints()))


    def coveredPoints(self):
        coveredPointList = []
        if self.antennaList:
            for antenna in self.antennaList:
                for coveredPoint in antenna.affectedPoints:
                    coveredPointList.append(coveredPoint)
            return list(set(coveredPointList))
        else:
            return None



    #return the most distant point from referencePoint in pointList
    def _farestFrom_(self,referencePoint,pointList):
        if len(pointList) > 0 :
            pointA = pointList[0]
            for point1 in pointList:
                if point1 != referencePoint and  self.distanceBetween(point1, referencePoint) > self.distanceBetween(pointA, referencePoint):
                    pointA = point1
            return pointA
        else:
            return None



    #return the antenna object at the position received
    def _antennaAt_(self,coordinate):
        for antenna in self.antennaList:
            if antenna.position == coordinate:
                return antenna


    #return an estimate distance of "near" points scanning all points
    #this value is used to estimate where is worth to put an antenna betewen 2 points
    def _defineSmallDistance_(self):
        distanceList = []
        visitedPoints = []
        for pt1 in self.pointList:
            for pt2 in self.pointList:
                if pt2 not in visitedPoints:
                    distanceList.append(self.distanceBetween(pt1, pt2))
            visitedPoints.append(pt1)
        mean = self._mean_(distanceList)

        return mean

    #return the mean
    def _mean_(self, list):
        sum = 0
        length = len(list)
        for i in list:
            sum += i
        return sum/float(length)




"""
X = (random.sample(range(1, 101), 100))
Y = (random.sample(range(1, 101), 100))
positionDesAntennes = []

i = 0

while i < len(X):
    positionDesAntennes.append((X[i],Y[i]))
    i+= 1
print("PointList = %s" %(positionDesAntennes))
"""
"""
start = time.time()
positionDesAntennes = ([(30,0),(10,10),(20,20),(30,40),(50,40)])

q = AlgorithmeRecuitState(positionDesAntennes,200,1)

while simulated_annealing_search(q,0.1,0.01,100) == None:
    print "Restart..."
    q = AlgorithmeRecuitState(positionDesAntennes,200,1)
end = time.time()
print '{} seconds'.format(end-start)

"""

"""
start = time.time()
positionDesAntennes = ([(30,0),(10,10),(20,20),(30,40),(50,40)])
q = AlgorithmeRecuitState(positionDesAntennes,200,1)
end = 0

while end-start > 5000000:
    while simulated_annealing_search(q,0.1,0.01,100) == None:
        print "Restart..."
        q = AlgorithmeRecuitState(positionDesAntennes, 200, 1)
    #if simulated_annealing_search(q,0.1,0.01,100) is better:
        #replace node
    end = time.time()
end = time.time()
print '{} seconds'.format(end-start)
"""

start = time.time()
positionDesAntennes = ([(30,0),(10,10),(20,20),(30,40),(50,40)])
#positionDesAntennes =[(486, 401), (88, 31), (489, 194), (174, 482), (276, 74), (250, 129), (402, 140), (374, 143), (328, 336), (14, 379), (441, 468), (362, 133), (256, 55), (7, 94), (469, 173), (100, 77), (42, 469), (252, 119), (51, 243), (204, 57), (456, 437), (292, 321), (107, 385), (94, 471), (69, 478), (280, 445), (285, 432), (20, 118), (421, 399), (68, 374), (212, 442), (416, 62), (171, 172), (460, 175), (499, 197), (161, 196), (435, 29), (228, 222), (258, 103), (106, 15), (481, 13), (312, 179), (266, 356), (130, 123), (154, 58), (194, 230), (425, 214), (159, 218), (413, 109), (450, 211), (183, 499), (259, 66), (253, 223), (49, 170), (308, 400), (241, 40), (338, 481), (93, 81), (384, 377), (431, 460), (390, 164), (76, 49), (30, 302), (492, 382), (136, 333), (124, 330), (223, 128), (363, 289), (487, 430), (78, 319), (172, 489), (263, 376), (57, 271), (339, 3), (168, 46), (257, 233), (485, 261), (25, 353), (109, 244), (197, 189), (235, 227), (142, 312), (86, 163), (265, 73), (278, 310), (316, 154), (394, 354), (403, 130), (34, 288), (46, 339), (301, 384), (125, 410), (412, 423), (420, 456), (237, 365), (50, 42), (97, 226), (104, 388), (182, 371), (131, 317)]
"""
import random
X = (random.sample(range(1, 501), 500))
Y = (random.sample(range(1, 501), 500))

positionDesAntennes = []
i = 0
while i < len(X):
    positionDesAntennes.append((X[i],Y[i]))
    i+= 1
    """
print("PointList = %s" %(positionDesAntennes))


q = AlgorithmeRecuitState(positionDesAntennes,200,1)
end = 0
bestnode = Node(q)
bestnode.f = 1000000000000000
while end-start < 10:
    node = simulated_annealing_search(q,0.1,0.01,100)
    while node == None:
        print "Restart..."
        q = AlgorithmeRecuitState(positionDesAntennes, 200, 1)
        node = simulated_annealing_search(q,0.1,0.01,100)

    if node.f < bestnode.f:
        bestnode = node
        q = AlgorithmeRecuitState(positionDesAntennes, 200, 1)
    end = time.time()
end = time.time()

bestnode.state.show()

print '{} seconds'.format(end-start)