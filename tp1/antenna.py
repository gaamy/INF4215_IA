
class Antenna:
    position = (int,int)
    radius = int
    affectedPoints = []

    def __init__(self,position,radius):
        self.position = position
        self.radius = radius


    def setAffectedPoints(self,pointList):
        pass

    def addPoint(self,newPoint):
        pass

    def deletePoint(self,unwantedPoint):
        pass