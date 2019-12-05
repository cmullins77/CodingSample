#Cassie Mullins, Project 0
def setup():
    size(500,500)
    
def draw():
    background(255,255,255)
    coords = [0+0j]
    index = 0
    x = mouseX
    y = mouseY
    h = 0
    if mouseY > 250:
        h = 255
    x = (x / (500/4.0)) - 2
    y = -((y / (500/4.0)) - 2)
    v = complex(x,y)
    for a in range(0,9):
        currentNum = 1
        for b in range(0,a):
            currentNum = currentNum * v
        numIndex = 2**a
        i = len(coords)
        for b in range(i-numIndex, i):
            oldNum = coords[b]
            newNum = oldNum + currentNum
            coords.append(newNum)
            newNum = oldNum - currentNum
            coords.append(newNum)
        index = len(coords) - 1
    for a in range(0,len(coords)):
        stroke(h,h,h)
        fill(h,123-((coords[a].imag)*50),123-((coords[a].real)*50))
        ellipse(((coords[a].real)+3)*(500/6.0),(-(coords[a].imag)+3)*(500/6.0),10,10)