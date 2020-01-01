# Cassie Mullins
# This is a simple ray tracing program that takes in text-files full of vertex coordinates 
# and shader information and generates images.
# To Run you will need to download Processing at: https://processing.org/download/
# Unzip the files and then open the processing app.
# In the top right corner there is a dropdown menu to choose the mode, by default it is Java.
# You will need to switch Processing to be in Python, so from that menu select Add Mode.
# Search for and download/install Python mode. Then switch to Python in the dropdown menu.

# Run the code by hitting the play button.
# There are 10 different scenes that can be rendered, choose between them by hitting the number keys.
# It may take around a minute for a scene to be rendered.


#Import all the Classes
from Hit import *
from Light import *
from Ray import *
from Scene import *
from Sphere import *
from Surface_Material import *
from Shape import *
from Vector import *
from Vector2D import *
from Triangle import *

def setup():
    global vector
    vector = Vector(0,0,0)
    size(500, 500) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)
    global camPosit
    global viewPlaneZ
    camPosit = Vector(0,0,0)
    viewPlaneZ = -1

# read and interpret the appropriate scene description .cli file based on key press
def keyPressed():
    if key == '1':
        interpreter("i1.cli")
    elif key == '2':
        interpreter("i2.cli")
    elif key == '3':
        interpreter("i3.cli")
    elif key == '4':
        interpreter("i4.cli")
    elif key == '5':
        interpreter("i5.cli")
    elif key == '6':
        interpreter("i6.cli")
    elif key == '7':
        interpreter("i7.cli")
    elif key == '8':
        interpreter("i8.cli")
    elif key == '9':
        interpreter("i9.cli")
    elif key == '0':
        interpreter("i10.cli")

def interpreter(fname):
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
    
    #Create the Scene that is being created
    global thisScene
    thisScene = Scene()
    # parse each line in the file in turn
    for line in lines:
        words = line.split()  # split the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            radius = float(words[1])
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            # Create a sphere and add it to list of shapes in scene
            newSphere = Sphere(radius,x,y,z,thisScene.currentMaterial, len(thisScene.shapeList))
            thisScene.shapeList.append(newSphere)
        elif words[0] == 'fov':
            #Set the Scene's fov & k
            thisScene.fov = float(words[1])
            thisScene.k = tan(radians(thisScene.fov/2.0))
        elif words[0] == 'background':
            #Save the background Col, default is black
            thisScene.backgroundCol = Vector(float(words[1]), float(words[2]), float(words[3]))
        elif words[0] == 'light':
            #Create a light and save to list of lights in scene
            newLight = Light(Vector(float(words[1]), float(words[2]), float(words[3])), Vector(float(words[4]), float(words[5]), float(words[6])))
            thisScene.lightList.append(newLight)
        elif words[0] == 'surface':
            #Create a new surface and set it as the current surface, to be applied to newly created shapes
            newSurface = Surface_Material(float(words[1]), float(words[2]), float(words[3]), float(words[4]), float(words[5]), float(words[6]), float(words[7]), float(words[8]), float(words[9]), float(words[10]), float(words[11]))
            thisScene.setMaterial(newSurface)
            #thisScene.materialList.append(newSurface)
        elif words[0] == 'begin':
            global currentShape
            currentShape = []
        elif words[0] == 'vertex':
            global currentShape
            currentShape.append(Vector(float(words[1]), float(words[2]), float(words[3])))
        elif words[0] == 'end':
            global currentShape
            if (len(currentShape) == 3):
                tri = Triangle(currentShape[0], currentShape[1], currentShape[2], thisScene.currentMaterial, len(thisScene.shapeList))
                thisScene.shapeList.append(tri)
        elif words[0] == 'write':
            render_scene()    # render the scene
            save(words[1])  # write the image to a file
            pass


# render the ray tracing scene
def render_scene():
    for j in range(height):
        for i in range(width):
            #Convert pixel coords to coords used in file
            x = (i * ((2*thisScene.k)/width)) - thisScene.k
            y = (j * ((2*thisScene.k)/height)) - thisScene.k

            #Create an Eye Ray at the point, use camera posit specified in setup, as well as viewplanez
            currentRay = Ray(Vector(x, y * -1, viewPlaneZ),camPosit)
            #Check if there's a hit with the ray, creates a hit list in scene
            thisScene.checkHit(currentRay, False)
            
            #If there was a hit do coloring, if not pick background color
            if (len(thisScene.hitList) > 0):
                #pix_color = color(1,1,1)
                #Choose hit closest to camera
                closestHit = pickHit(thisScene.hitList, camPosit)
                #set pixel color to appropriate color based on shading formulas
                pix_color = calculateColor(closestHit, 0, camPosit)
                pix_color = color(pix_color.x, pix_color.y, pix_color.z)
            else:
                pix_color = thisScene.backgroundCol
                pix_color = color(pix_color.x, pix_color.y, pix_color.z)
            set (i, j, pix_color)         # fill the pixel with the calculated color
    
#finds relevant hit
def pickHit(hitList, otherPoint):
    #Starts with first hit in list
    currentHit = hitList[0]
    #Loops through hits and if the hit is closert to camera
    for i in range(1,len(hitList)):
        newHit = hitList[i]
        if (vector.Dist(newHit.locationVector, otherPoint) < vector.Dist(currentHit.locationVector, otherPoint)):
            currentHit = newHit
    return currentHit

#calculates color based on closest hit
def calculateColor(currentHit, depth, view):
    #Set initial light and pixel color to 0
    
    #Get surface color from the hit
    surfaceCol = currentHit.material.diffCol
    ambiCol = currentHit.material.ambiCol
    specCol = currentHit.material.specCol
    E = vector.Sub(camPosit, currentHit.locationVector)
    E.Normalize()
    
    totalLightCol = Vector(0,0,0)
    totalPixelCol = Vector(ambiCol.x,ambiCol.y,ambiCol.z)
    #totalPixelCol = Vector(0,0,0)
    krefl = currentHit.material.krefl
    #totalPixelCol = PVector(0,0,0)
    #For each light calculate what the color of the pixel would be with just that light, and then add it to the total color
    for j in range(len(thisScene.lightList)):
        aLight = thisScene.lightList[j]
        currentLight = Light(aLight.posit, aLight.col)
        
        #shadows
        ray = Ray(Vector(currentHit.locationVector.x, currentHit.locationVector.y, currentHit.locationVector.z), Vector(currentLight.posit.x, currentLight.posit.y, currentLight.posit.z))
        #shadow = thisScene.checkShadow(ray, currentHit.objNum)
        shadow = thisScene.checkHit(ray, False)
        if (shadow):
            shadowHit = False
            for k in range(0, len(thisScene.hitList)):
                cHit = thisScene.hitList[k]
                t = cHit.t
                if (t > 0.01 and t < .99 and currentHit.objNum != cHit.objNum):
                    shadowHit = True
            shadow = shadowHit
            

        if (not shadow):
            #Get the l vector, which is the light position - the hit position, and then normalize
            l = vector.Sub(currentLight.posit, currentHit.locationVector)
            l.Normalize()
            
            specVector = Vector(0,0,0)
            #specular
            if (not shadow):
                R1 = vector.Dot(currentHit.n, l)
                R2 = vector.Mult(currentHit.n, 2)
                R3 = vector.Mult(R2, R1)
                R = vector.Sub(R3, l)
                R.Normalize()
        
                aNum = vector.Dot(E, R)
                p = currentHit.material.p
                bNum = max(0, aNum)**(p)
                
                highlightCol = vector.Mult(specCol, bNum)
                specVector = vector.ElemMult(highlightCol, currentLight.col)
                
            diffVector = Vector(0,0,0)
            if (not shadow):
                #Find the N.L
                aNum = vector.Dot(l, currentHit.n)
        
                #Find wheterh N.L is negative
                bNum = max(0, aNum)
                
                #Get Light Color
                lightCol = currentLight.col
                
                #Multiply by light color
                diffVector = vector.Mult(lightCol, bNum)
                diffVector = vector.ElemMult(diffVector, surfaceCol)
            
            thisLightCol = vector.Add(diffVector, specVector)
            totalPixelCol = vector.Add(totalPixelCol, thisLightCol)
            # #ElementWise Multiplication of surface Color and light color
            # diffPixelCol = vector.ElemMult(surfaceCol, lightCol)
            # specPixelCol = highlightCol
            # #Add colors to total
            # newPixelCol = vector.Add(diffPixelCol, specPixelCol)
            # totalPixelCol = vector.Add(totalPixelCol,newPixelCol)
    if (krefl != 0 and depth < 11):
        crefl = getReflection(currentHit, depth, view)
        reflectColor = Vector(crefl.x * krefl, crefl.y *krefl, crefl.z*krefl)
        totalPixelCol = vector.Add(totalPixelCol, reflectColor)
            
            
    #Return new color
    return Vector(totalPixelCol.x, totalPixelCol.y, totalPixelCol.z)

def getReflection(currentHit, depth, origin):
    currentLocation = currentHit.locationVector
    V = vector.Sub(origin, currentLocation)
    V.Normalize()
    R = vector.Sub(vector.Mult(currentHit.n, 2* vector.Dot(V, currentHit.n)), V)
    #R.Normalize()
    point1 = vector.Add(R,currentLocation)
    #point1.Normalize()
    ray = Ray(point1, currentLocation)
    thisScene.checkHit(ray,True)
    if (len(thisScene.hitList) > 0):
        #Choose hit closest to currentHit
        closestHit = pickHit(thisScene.hitList, currentLocation)
        #set pixel color to appropriate color based on shading formulas
        pix_color = calculateColor(closestHit, depth + 1, currentLocation)
    else:
        pix_color = thisScene.backgroundCol
    
    return pix_color
    
# def getReflection(currentHit, depth, camPosit):
#     V = vector.Sub(camPosit, currentHit.locationVector)
#     V.Normalize()
#     R1 = vector.Dot(currentHit.n, V)
#     R2 = vector.Mult(currentHit.n, 2)
#     R3 = vector.Mult(R2, R1)
#     R = vector.Sub(R3, V)
#     R.Normalize()
#     secondPoint = vector.Add(currentHit.locationVector, R)
#     newRay = Ray(secondPoint, currentHit.locationVector)
#     global thisScene
#     thisScene.checkHit(newRay)
#     if (len(thisScene.hitList) > 0):
#         #Choose hit closest to point
#         closestHit = pickHit(thisScene.hitList, currentHit.locationVector)
#         #set pixel color to appropriate color based on shading formulas
#         pix_color = calculateColor(closestHit, depth + 1, currentHit.locationVector)
#     else:
#         pix_color = thisScene.backgroundCol
#     return pix_color

# should remain empty for this assignment
def draw():
    pass
