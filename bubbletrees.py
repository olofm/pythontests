import pygame, sys, math, random
from pygame.locals import *

# Click on the screen to plant a bubbletree
# Spacebar to level up


# framerate
FPS = 30

# window
WINDOWWIDTH = 1600
WINDOWHEIGHT = 1000

# other
STARTRADIUS = 10
BGCOLOR = (0,0,0)
trees = []
TREEMAX = 7
FRICTION = 1.5
MAXWIND = 3
WINDCHANGE = 0.4


# make colors
COLORS = []
C0     = (139, 69, 19)

colors = []
colors.append(C0)
for i in range(0,TREEMAX+1):
    c = (round(255*(i/TREEMAX)), 0, round(255*((TREEMAX-i)/TREEMAX)))
    colors.append(c)
COLORS.append(colors)

colors = []
colors.append(C0)
for i in range(0,TREEMAX):
    c = (round(255*((TREEMAX-i)/TREEMAX)), 0, round(255*(i/TREEMAX)))
    colors.append(c)
COLORS.append(colors)

colors = []
colors.append(C0)
for i in range(0,TREEMAX+1):
    c = (0, round(255*(i/TREEMAX)), round(255*((TREEMAX-i)/TREEMAX)))
    colors.append(c)
COLORS.append(colors)

colors = []
colors.append(C0)
for i in range(0,TREEMAX):
    c = (0, round(255*((TREEMAX-i)/TREEMAX)), round(255*(i/TREEMAX)))
    colors.append(c)
COLORS.append(colors)

colors = []
colors.append(C0)
for i in range(0,TREEMAX+1):
    c = (round(255*(i/TREEMAX)), round(255*((TREEMAX-i)/TREEMAX)), 0)
    colors.append(c)
COLORS.append(colors)

colors = []
colors.append(C0)
for i in range(0,TREEMAX):
    c = (round(255*((TREEMAX-i)/TREEMAX)), round(255*(i/TREEMAX)), 0)
    colors.append(c)
COLORS.append(colors)



def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    NTREES = 0
    WIND = 0
    
    # main loop
    while True:
        
        # draw background
        DISPLAYSURF.fill(BGCOLOR)

        # check input events
        for event in pygame.event.get():

            # quit
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # level up
            elif event.type == KEYUP and event.key == K_SPACE:
                print('Level up!')
                for t in trees:
                    t.levelUp()
                    print('tree number '+ str(trees.index(t)+1) + ' has ' + str(len(t.getBubbles())) + ' bubbles')

            # left click release
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos
                print(mousex, mousey)
                NTREES += 1
                if NTREES is 6:
                    NTREES = 0
                newtree = makeTree(mousex, mousey, COLORS[NTREES-1])
                trees.append(newtree)

        # update frame
        
        WIND = WIND + random.uniform(-WINDCHANGE, WINDCHANGE)
        if WIND > MAXWIND:
            WIND = MAXWIND
        elif WIND < -MAXWIND:
            WIND = -MAXWIND
 
        for t in trees:
            t.updatePos()
            t.addWind(WIND)
            t.drawStem()
            t.draw()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def newWind(wind, maxwind):
    wind = wind + random.uniform(-1, 1)
    if wind > maxwind:
        wind = maxwind
    elif wind < -maxwind:
        wind = -maxwind

class Tree(object):
    
    bubbleratio = 5/8
    treespread = math.pi/3
    bubbledev = 0.1
    
    level = 1
    bubbles = []
    root = 0
    colors = 0
    
    def __init__(self, x, y, colors):
        self.bubbles = []
        self.root = makePoint(x, y)
        self.colors = colors
        mainbubble = makeBubble(self.root, 0, self.bubbleratio, self.bubbledev, self.treespread, self.colors)
        self.bubbles.append(mainbubble)

    def levelUp(self):
        if self.level < TREEMAX:
            self.level += 1
            newbubbles = []
            self.root.increase(self.bubbleratio)
            for b in self.bubbles:
                b.increase(self.bubbleratio)
            self.updatePos()
            for b in self.bubbles:
                newbubbles.append(b)
                if b.getLevel() is self.level-1:
                    newb1 = makeBubble(b, -self.treespread, self.bubbleratio, self.bubbledev, self.treespread, self.colors)
                    newb2 = makeBubble(b, 0, self.bubbleratio, self.bubbledev, self.treespread, self.colors)
                    newb3 = makeBubble(b, self.treespread, self.bubbleratio, self.bubbledev, self.treespread, self.colors)
                    newbubbles.append(newb1)
                    newbubbles.append(newb2)
                    newbubbles.append(newb3)
            self.bubbles = newbubbles
            

    def draw(self):
        for b in self.bubbles:
            b.draw()

    def drawStem(self):
        for b in self.bubbles:
            b.drawStem()

    def updatePos(self):
        for level in range(1,self.level+1):
            for b in self.bubbles:
                if b.getLevel() is level:
                    b.go()

    def addWind(self, wind):
        for b in self.bubbles:
            b.addWind(wind)
                    
    def getBubbles(self):
        return self.bubbles

def makeTree(x, y, colors):
    tree = Tree(x, y, colors)
    return tree

class Bubble(object):
    radius = 1
    level = 0
    parent = 0
    phi = -math.pi/2
    colors = 0
    x, y = 0,0
    aimx, aimy = 0, 0
    vx, vy = 0, 0
    ax, ay = 0, 0

    def __init__(self, parent, bend, bubbleratio, bubbledev, treespread, colors):
        self.parent = parent
        self.level = parent.getLevel()+1
        self.colors = colors
        self.radius = parent.getRadius()*bubbleratio*random.uniform(1-bubbledev/2, 1+bubbledev/2)
        px, py = parent.getPos()
        r = parent.getRadius()*2
        phi = -math.pi/2
        if self.level > 1:
            phi = parent.getPhi() + bend + random.uniform(-treespread/3, treespread/3)
        self.aimx = px + r * math.cos(phi)
        self.aimy = py + r * math.sin(phi)
        self.x = px + r/2 * math.cos(phi)
        self.y = py + r/2 * math.sin(phi)
        self.phi = phi

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, self.colors[self.level], (round(self.x), round(self.y)), round(self.radius), 0)

    def drawStem(self):
        pygame.draw.line(DISPLAYSURF, self.colors[0], (round(self.x), round(self.y)), (round(self.parent.getX()), round(self.parent.getY())), round(self.radius/2))

    def getPos(self):
        return self.x, self.y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getLevel(self):
        return self.level

    def getRadius(self):
        return self.radius

    def getPhi(self):
        return self.phi

    def increase(self, bubbleratio):
        self.radius = self.radius/bubbleratio

    def updatePos(self):
        px, py = self.parent.getPos()
        r = self.parent.getRadius()*2
        if self.level is 1:
            r = self.parent.getRadius()*3
        self.x = px + r * math.cos(self.phi)
        self.y = py + r * math.sin(self.phi)

    def go(self):
        px, py = self.parent.getPos()
        r = self.parent.getRadius()*2
        if self.level is 1:
            r = self.parent.getRadius()*3
        self.aimx = px + r * math.cos(self.phi)
        self.aimy = py + r * math.sin(self.phi)
        self.ax = (self.aimx - self.x)/self.radius
        self.ay = (self.aimy - self.y)/self.radius
        self.vx = self.vx/FRICTION + self.ax
        self.vy = self.vy/FRICTION + self.ay
        self.x = self.x + self.vx
        self.y = self.y + self.vy

    def addWind(self, wind):
        self.vx = self.vx + (wind+random.uniform(-WINDCHANGE,WINDCHANGE))/self.radius
    
def makeBubble(parent, bend, bubbleratio, bubbledev, treespread, colors):
    bubble = Bubble(parent, bend, bubbleratio, bubbledev, treespread, colors)
    return bubble

class Point(object):
    x,y = 0,0
    radius = 1
    
    def __init__(self, x, y):
        self.x,self.y = x,y
        self.radius = STARTRADIUS

    def getPos(self):
        return self.x, self.y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getLevel(self):
        return 0
    
    def getRadius(self):
        return self.radius

    def getPhi(self):
        return -math.pi/2

    def increase(self, bubbleratio):
        self.radius = self.radius/bubbleratio
    
def makePoint(x,y):
    point = Point(x,y)
    return point
    
if __name__ == '__main__':
    main()
