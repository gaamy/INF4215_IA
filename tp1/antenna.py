import math

from point import *

class Antenna:

    def __init__(self):
        self.radius = 1
        self.affectedPoints = []

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
        self.deletePoint(self.farPoint())

    def updateAntenna(self):
        amountOfAfectedPoints = len(self.affectedPoints)
        if amountOfAfectedPoints <= 0:
            self.radius = 0
            self.position = (0,0)
        elif amountOfAfectedPoints == 1:
            self.position = self.affectedPoints[0]
            self.radius = 1
        else:
            self.position = self.centroid(self.affectedPoints)
            self.radius = self.distanceBetween(self.position,self.farPoint())


    #return the central point of a group of points
    def centroid(self,pointList):
        if len(pointList) > 0:
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
        if len(self.affectedPoints) > 0 :
            pointA = self.affectedPoints[0]
            for point1 in self.affectedPoints:
                if self.distanceBetween(point1,self.position) > self.distanceBetween(pointA,self.position):
                    pointA = point1
            return pointA
        else:
            return self.position