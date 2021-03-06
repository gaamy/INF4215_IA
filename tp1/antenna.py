import math

from point import *
import random

class Antenna:

    def __init__(self):
        self.radius = 1
        self.affectedPoints = []
        self.position = Point(0,0)

    def addPointList(self,pointlist):
        self.affectedPoints.extend(pointlist)
        self.updateAntenna()

    def addPoint(self,newPoint):
        self.affectedPoints.append(newPoint)
        self.updateAntenna()

    def deletePoint(self,unwantedPoint):
        if unwantedPoint in self.affectedPoints:
            self.affectedPoints.remove(unwantedPoint)
        self.updateAntenna()

    def shrink(self):
        pointToRemove = self.farPoint()
        if pointToRemove != None:
            self.deletePoint(pointToRemove)

    def updateAntenna(self):
        amountOfAfectedPoints = len(self.affectedPoints)
        if amountOfAfectedPoints <= 0:
            self.radius = 0
            self.position = Point(0,0)
        elif amountOfAfectedPoints == 1:
            self.position = self.affectedPoints[0]
            self.radius = 1
        else:
            self.position = self.centroid(self.affectedPoints)
            self.radius = self.distanceBetween(self.position,self.farPoint())

    def growRandom(self,pointList,maxRWorth):
        self.radius += random.randint(1, int(maxRWorth))
        for point in pointList:
            if self.distanceBetween(self.position,point) <= self.radius:
                self.affectedPoints.append(point)
                #self.updateAntenna()



    #return the central point of a group of points
    def centroid(self,pointList):
        if pointList :
            sum_x = 0
            sum_y = 0
            length = len(pointList)
            for point in pointList:
                sum_x += point.x
                sum_y += point.y
            centroid = Point(sum_x/length, sum_y/length)
            return centroid
        return self.position

    #Return the distance between 2 points
    def distanceBetween(self,pt1,pt2):
        return math.sqrt( (pt2.x-pt1.x)**2 + (pt2.y-pt1.y)**2 )

    #return the most distant point covered by the antenna  in pointList
    def farPoint(self):
        if self.affectedPoints :
            pointA = self.affectedPoints[0]
            for point1 in self.affectedPoints:
                if self.distanceBetween(point1,self.position) > self.distanceBetween(pointA,self.position):
                    pointA = point1
            return pointA
        else:
            return None