class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    #this is what is printed if called in print() equivalent to .toString() from java
    def __str__(self):
    	return "({0},{1})".format(self.x, self.y)

