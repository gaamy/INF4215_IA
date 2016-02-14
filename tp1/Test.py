import unittest

from antenna import *

class AntennaTestCase(unittest.TestCase):
    def setUp(self):
        self.antenna = Antenna()

    def tearDown(self):
        pass

    def test_add_single_point_when_empty(self):
        self.antenna.addPoint(Point(1,1))
        result = self.antenna.affectedPoints[0] == Point(1,1)
        self.assertTrue(result, 'wrong element added')
        self.assertEquals(len(self.antenna.affectedPoints) , 1, 'wrong size')
        self.assertEquals(self.antenna.radius, 1,'Wrong radius')
        self.assertEquals(self.antenna.position, Point(1,1),'Wrong antenna position')

    def test_add_single_point_when_not_empty(self):
        self.antenna.addPoint(Point(10,10))
        self.antenna.addPoint(Point(30,30))

        result = Point(30,30) in self.antenna.affectedPoints
        self.assertTrue(result, 'wrong element added')
        self.assertEquals(len(self.antenna.affectedPoints) , 2, 'wrong size')
        self.assertEquals(self.antenna.radius, math.sqrt(2)*10 ,'Wrong radius')
        self.assertEquals(self.antenna.position, Point(20,20),'Wrong antenna position')

