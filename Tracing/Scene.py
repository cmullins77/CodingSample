from Surface_Material import *
from Light import *
from Hit import *
from Vector import *
from Vector2D import *
class Scene:
    
    def __init__(self):
        self.shapeList = []
        self.lightList = []
        self.backgroundCol = Vector(0,0,0)
        self.fov = 0
        self.materialList = []
        self.currentMaterial = Surface_Material(0,0,0, 0, 0, 0, 0,0,0,0,0)
        
    def setMaterial(self, newMaterial):
        self.currentMaterial = newMaterial

    #Take in D of ray
    def checkHit(self, ray, reflection):
        #Grab values from ray
        x1 = ray.point1.x
        y1 = ray.point1.y
        z1 = ray.point1.z
        x0 = ray.point0.x
        y0 = ray.point0.y
        z0 = ray.point0.z
        self.hitList = []
        hitFound = False
        #For each shape check for intersection
        for i in range(len(self.shapeList)):
            currentShape = self.shapeList[i]
            hit = currentShape.checkHit(x0, y0, z0, x1, y1, z1)
            if (hit):
                self.hitList.append(currentShape.hit)
                hitFound = True
        return hitFound