from Vector import *
from Vector2D import *
class Surface_Material:
    def __init__(self, dR, dG, dB, aR, aG, aB, sR, sG, sB, p, krefl):
        self.diffCol = Vector(dR, dG, dB)
        self.ambiCol = Vector(aR, aG, aB)
        self.specCol = Vector(sR,sG,sB)
        self.p = p
        self.krefl = krefl