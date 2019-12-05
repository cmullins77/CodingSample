from Vector import *
from Vector2D import *
class Ray:
    def __init__(self, newPoint1, newPoint0):
        self.point0 = Vector(newPoint0.x, newPoint0.y, newPoint0.z)
        self.point1 = Vector(newPoint1.x, newPoint1.y, newPoint1.z)
        