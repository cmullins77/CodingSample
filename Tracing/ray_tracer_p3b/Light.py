from Vector import *
from Vector2D import *
class Light:
    def __init__(self, newPosit, newCol):
        self.col = Vector(newCol.x, newCol.y, newCol.z)
        self.posit = Vector(newPosit.x, newPosit.y, newPosit.z)