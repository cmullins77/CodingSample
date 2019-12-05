class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def ElemMult(self, v1, v2):
        return Vector2D(v1.x * v2.x, v1.y *v2.y)
    
    def Mult(self, v, s):
        return Vector2D(v.x * s, v.y * s)
    
    def Sub(self, v1,v2):
        return Vector2D(v1.x - v2.x, v1.y - v2.y)
    
    def Add(self, v1, v2):
        return Vector2D(v1.x + v2.x, v1.y + v2.y)
    
    def Mag(self):
        return sqrt(self.x**2 + self.y**2)
    
    def Div(self, v, s):
        return Vector2D(v.x / float(s), v.y / float(s))
    
    def Dot(self, v1, v2):
        return v1.x*v2.x + v1.y*v2.y
    
    def Normalize(self):
        magnitude = float(self.Mag())
        self.x = self.x/magnitude
        self.y = self.y/magnitude
        
    def Dist(self, v1, v2):
        return sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)