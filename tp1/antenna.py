import math

class Antenna:
    position = (int,int)
    radius = int
    affectedPoints = []

    def __init__(self,position):
        self.position = position
        self.radius = 1

    def __init__(self,pointList):
        self.affectedPoints = pointList
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
        if len(self.affectedPoints) <= 0:
            self.radius = 0
            self.position = (0,0)
        else:
            self.position = self.centroid(self.affectedPoints)
            self.radius = self.distanceBetween(self.position, max(self.affectedPoints))


    #return the central point of a group of points
    def centroid(self,pointList):
        sum_x = 0
        sum_y = 0
        length = len(pointList)
        for point in pointList:
            sum_x += point[0]
            sum_y += point[1]
        return sum_x/float(length), sum_y/float(length)

    #Return the distance between 2 points
    def distanceBetween(self,pt1,pt2):
        return math.sqrt( (pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2 )

    #return the most distant point covered by the antenna  in pointList
    def farPoint(self):
        if len(self.affectedPoints) > 0 :
            pointA = self.affectedPoints[0]
            for point1 in self.affectedPoints:
                if self.distanceBetweenPoints(point1,self.position) > self.distanceBetweenPoints(pointA,self.position):
                    pointA = point1
            return pointA
        else:
            return None