from Shape import *
from Hit import *
from Vector import *
from Vector2D import *
class Triangle (Shape):
    
    def __init__(self, newPoint0, newPoint1, newPoint2, newMaterial, objNum):
        self.point0 = Vector(newPoint0.x, newPoint0.y, newPoint0.z)
        self.point1 = Vector(newPoint1.x, newPoint1.y, newPoint1.z)
        self.point2 = Vector(newPoint2.x, newPoint2.y, newPoint2.z)
        self.objNum = objNum
        self.vector = Vector(0,0,0)
        A = self.vector.Sub(self.point1, self.point0)
        B = self.vector.Sub(self.point2, self.point0)
        C = self.vector.Cross(A,B)
        C.Normalize()
        C = self.vector.Mult(C,-1)
        self.n = C
        self.material = newMaterial
        xy = self.getArea(Vector2D(self.point0.x, self.point0.y), Vector2D(self.point1.x, self.point1.y), Vector2D(self.point2.x, self.point2.y))
        yz = self.getArea(Vector2D(self.point0.y, self.point0.z), Vector2D(self.point1.y, self.point1.z), Vector2D(self.point2.y, self.point2.z))
        zx = self.getArea(Vector2D(self.point0.z, self.point0.x), Vector2D(self.point1.z, self.point1.x), Vector2D(self.point2.z, self.point2.x))
        if (xy > yz):
            if xy > zx:
                pointA = Vector2D(self.point0.x, self.point0.y)
                pointB = Vector2D(self.point1.x, self.point1.y)
                pointC = Vector2D(self.point2.x, self.point2.y)
                self.mode = 1
                self.Area = xy
            else:
                pointA = Vector2D(self.point0.z, self.point0.x)
                pointB = Vector2D(self.point1.z, self.point1.x)
                pointC = Vector2D(self.point2.z, self.point2.x)
                self.mode = 2
                self.Area = zx
        else:
            if (yz > zx):
                pointA = Vector2D(self.point0.y, self.point0.z)
                pointB = Vector2D(self.point1.y, self.point1.z)
                pointC = Vector2D(self.point2.y, self.point2.z)
                self.mode = 3
                self.Area = yz
            else:
                pointA = Vector2D(self.point0.z, self.point0.x)
                pointB = Vector2D(self.point1.z, self.point1.x)
                pointC = Vector2D(self.point2.z, self.point2.x)
                self.mode = 2
                self.Area = zx
        self.pA = pointA
        self.pB = pointB
        self.pC = pointC
        self.c = (pointC.x - pointA.x)*(pointB.y - pointA.y) - (pointC.y - pointA.y)*(pointB.x - pointA.x)
        self.a = (pointA.x - pointB.x)*(pointC.y - pointB.y) - (pointA.y - pointB.y)*(pointC.x - pointB.x)
        self.b = (pointB.x - pointC.x)*(pointA.y - pointC.y) - (pointB.y - pointC.y)*(pointA.x - pointC.x)
        
    #formula for plane: (n.x)*(point1.x - point0.x) + (n.y)*(point1.y - point0.y) + (n.z)*(point1.z - point0.z) - (n.x*point0.x + n.y*point0.y + n.z*point0.z) = 0
    #t = - ((n.x)*(point1.x - point0.x) + (n.y)*(point1.y - point0.y) + (n.z)*(point1.z - point0.z))/()
    #t = ((point0 - originRay)dot n)/(rayPoint dot n)
    #t = (PVector.dot(PVector.sub(point0 - originRay), n)/(PVector.dot(rayPoint, n)
    def getArea(self, p0, p1, p2):
        return abs(((p0.x)*(p1.y - p2.y) + (p1.x)*(p2.y - p0.y) + (p2.x)*(p0.y - p1.y))/2)
    
    def checkHit(self, x0, y0, z0, x1, y1, z1):
        hitFound = False
        hitList = []
        originRay = Vector(x0,y0,z0)
        rayPoint = Vector(x1,y1,z1)
        check = self.vector.Dot(rayPoint, self.n)
        if (check != 0):
            # O = originRay
            # R = self.vector.Sub(rayPoint, originRay)
            # D = self.vector.Dot(self.n, self.point0)
            # aNum = self.vector.Dot(self.n, O)
            # bNum = D + aNum
            # cNum = self.vector.Dot(self.n, R)
            # t = -1 * bNum/cNum
            t = (self.vector.Dot(self.vector.Sub(self.point0, originRay), self.n) + (self.vector.Dot(self.n, originRay)))/check
            if (t > 0):
                hitPoint = self.vector.Add(originRay, self.vector.Mult(self.vector.Sub(rayPoint, originRay), t))
                
                pointA = self.pA
                pointB = self.pB
                pointC = self.pC
                mode = self.mode
                if (mode == 1):
                    pointQ = Vector2D(hitPoint.x, hitPoint.y)
                elif (mode == 2):
                    pointQ = Vector2D(hitPoint.z, hitPoint.x)
                else:
                    pointQ = Vector2D(hitPoint.y, hitPoint.z)
                d = (pointQ.x - pointA.x)*(pointB.y - pointA.y) - (pointQ.y - pointA.y)*(pointB.x - pointA.x)
                c = self.c
                if (c >= 0 and d >= 0) or (c <= 0 and d <= 0):
                    d = (pointQ.x - pointB.x)*(pointC.y - pointB.y) - (pointQ.y - pointB.y)*(pointC.x - pointB.x)
                    a = self.a
                    if (a >= 0 and d >= 0) or (a <= 0 and d <= 0):
                        d = (pointQ.x - pointC.x)*(pointA.y - pointC.y) - (pointQ.y - pointC.y)*(pointA.x - pointC.x)
                        b = self.b
                        if (b >= 0 and d >= 0) or (b <= 0 and d <=0):
                            newHit = Hit(hitPoint, self.n, self.material, self.objNum, t)
                            self.hit = newHit
                            hitFound = True
        return hitFound