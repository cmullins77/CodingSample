class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.l = [x,y,z]
        
    def ElemMult(self, v1, v2):
        return Vector(v1.x * v2.x, v1.y *v2.y, v1.z *v2.z)
    
    def Mult(self, v, s):
        return Vector(v.x * s, v.y * s, v.z * s)
    
    def Sub(self, v1,v2):
        return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
    
    def Add(self, v1, v2):
        return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
    
    def Mag(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def Div(self, v, s):
        return Vector(v.x / float(s), v.y / float(s), v.z / float(s))
    
    def Dot(self, v1, v2):
        return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
    
    def Cross(self, v1, v2):
        return  Vector(v1.y*v2.z-v1.z*v2.y, v1.z*v2.x - v1.x*v2.z, v1.x*v2.y - v1.y*v2.x)
    
    def Normalize(self):
        magnitude = float(self.Mag())
        if (magnitude != 0):
            self.x = self.x/magnitude
            self.y = self.y/magnitude
            self.z = self.z/magnitude
        
    def Dist(self, v1, v2):
        return sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2 + (v1.z - v2.z)**2)