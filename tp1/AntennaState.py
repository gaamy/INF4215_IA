# TP1 Couverture des antennes, version arboressante
#
# Author: Gabriel Amyot & Francis Rivest
#

from node import *
from state import *
from antenna import *
from point import *
from astar_search import *

import math

class AntennaState(State):


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

    #Antenna problem solution search
    #def search(self,points,K,C):

        #self.K = K
        #self.C = C
        #self.pointList = points
        #self.smallDistance = self._defineSmallDistance_()
        #return  astar_search(self)



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
        return False
        """
        if self.counter > self.threshold and self.coveredPoints == len(self.pointList):
        #if self.counter > self.threshold :
            return True
        else:
            return False
        """

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

                print("-----Antenna # %s"  %(self.antennaList.index(antenna)))
                print(" position= (%s,%s) " %(antenna.position.x,antenna.position.y))
                print(" r=%s" %(antenna.radius))
                print("--------------------------------------")






    # Returns a list of possible actions with the current state
    def possibleActions(self):
        actionList = []
        #action 1 : ajouter antenne sur 1 point
        for point in self.uncoveredPoints():
            actionList.append(('addSimpleAntenna',point))
        #action 2: antenne entre les 2 point les plus proches non couverts
        visitedPoints = []
        for pt1 in self.uncoveredPoints():
            for pt2 in self.uncoveredPoints():
                if pt1 != pt2 and pt2 not in visitedPoints :
                    if self.distanceBetween(pt1, pt2) <= self.smallDistance:
                        actionList.append(('addAntennaBetween2',pt1,pt2))
            visitedPoints.append(pt1)
        #action 3 et 4
        if len(self.antennaList) > 0:
            for antenna in self.antennaList:
                if len(antenna.affectedPoints) > 0:
                    #action 3: entre les antennes existantes, ajouter le point le plus proche de l'antenne non couvert
                    actionList.append(('growAntenna',antenna.position))
                    #action 4: entre les antennes existantes, retirer le point le plus loin couvert par l'antenne
                    actionList.append(('shrinkAntenna',antenna.position))
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
            antenna = self._antennaAt_(antennaPosition)
            antenna.addPoint(nearestPoint)
        elif actionName == 'shrinkAntenna':
            oldAntennaPosition = action[1]
            oldAntenna = self._antennaAt_(oldAntennaPosition)
            oldAntenna.shrink()
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
        return 0
        """
        if self.coveredPoints() != None:


            e = len(self.pointList)
            t = self.coveredPoints()
            a = len(t)

            amountOfRemainingPoints = len(self.pointList) - len(self.coveredPoints())
            return amountOfRemainingPoints * self.K
        else:
            return len(self.pointList)*self.K
        """

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
            return referencePoint

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

    # Return the coordinate in between 2 points
    #def _middlePoint_(self,point1,point2):
        #xm = (point1[0]+point2[0])/float(2)
        #ym = (point1[1]+point2[1])/float(2)
        #return (xm,ym)

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



initialState = AntennaState([(30,0),(10,10),(20,20),(30,40),(50,40)],200,1)

solution = astar_search(initialState)


print("Solution  is %s  " % (solution))


