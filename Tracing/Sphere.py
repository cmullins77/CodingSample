from Shape import *
from Hit import *
from Vector import *
from Vector2D import *
class Sphere (Shape):
    
    def __init__(self, newRadius, newX, newY, newZ, newMaterial, objNum):
        self.radius = newRadius
        self.x = newX
        self.y = newY
        self.z = newZ
        self.material = newMaterial
        self.objNum = objNum

    
    def checkHit(self, x0, y0, z0, x1, y1, z1):
        hitFound = False
        newHitList = []
        # center = PVector(self.x, self.y, self.z)
        # ray = PVector(dx, dy, dz)
        
        centerX = self.x
        centerY = self.y
        centerZ = self.z
        radius = self.radius
        a = (x1 - x0)**2 + (y1 - y0)**2 + (z1-z0)**2
        b = 2 * ((x1 - x0)*(x0 - centerX) + (y1 - y0)*(y0 - centerY) + (z1-z0)*(z0 - centerZ))
        c = centerX**2 + centerY**2 + centerZ**2 + x0**2 + y0**2 + z0**2 - 2*(centerX*x0 + centerY*y0 + centerZ*z0) - radius**2
        #Calculate Z
        # var1 = (2*centerX*dx + 2*centerY*dy + 2*centerZ*dz)
        # var2 = (-2*centerX*dx-2*centerY*dy-2*centerZ*dz)**2
        # var3 = var2-(4*(dx**2 + dy**2 + dz**2)*(centerX**2+centerY**2+centerZ**2-radius**2))
        # var4 = 2*(dx**2+dy**2+dz**2)
        var1 = b * -1
        var3 = b**2 - 4 * a * c
        var4 = 2 * a
        if (var3 >= 0 and var4 != 0):
            #Calculate T and use that to calculate x,y,z
            t = (var1 - sqrt(var3))/var4
            if (t > 0):
                x = x0 + (x1 - x0) * t
                y = y0 + (y1 - y0) * t
                z = z0 + (z1 - z0) * t
                
                #Create normal and normalize
                n = Vector(x - centerX, y - centerY, z - centerZ)
                n.Normalize()
                
                t2 = (var1 + sqrt(var3))/var4
                #Create Hit
                self.hit = Hit(Vector(x,y,z), n, self.material, self.objNum, t)
                hitFound = True
        return hitFound
    
    