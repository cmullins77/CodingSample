from Vector import *
from Vector2D import *
class Hit:
    def __init__(self, newPosit,newN, newMaterial, objNum, t):
        self.locationVector = Vector(newPosit.x, newPosit.y, newPosit.z)
        self.n = newN
        self.material = newMaterial
        self.objNum = objNum
        self.t = t