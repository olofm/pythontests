import pygame, sys, math, random
from pygame.locals import *


FPS = 60
WINDOWWIDTH = 700
WINDOWHEIGHT = 500
BORDER = 100
NPEOPLE = 30
NHOUSES = 0
FLOORSIZE = 40
ROOMSIZE = 50


# house colors
#           R   G   B
HC1     = (200,  0, 50)
HC2     = ( 50,  0,200)
HC3     = (200, 50,  0)
HOUSECOLORS = (HC1, HC2, HC3)
WINDOW  = (255,255,128)

# skin colors
#           R   G   B
SC1     = (255,255,128)
SC2     = (128,104,103)
SC3     = (100, 75, 50)
SC4     = (239,208,207)
SKINCOLORS = (SC1,SC2,SC3,SC4)

# clothes colors
#           R   G   B
CC1     = (  0,  0,128)
CC2     = (128,  0,  0)
CC3     = (128,  0,128)
CC4     = (128, 50,  0)
CLOTHESCOLORS = (CC1,CC2,CC3,CC4)

# other colors
BGCOLOR = (  0,  0,  0)
SELCOL  = (128,128,200)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # selection box
    SELX = 0
    SELY = 0
    mousex = 0
    mousey = 0
    SELBOX = 0
    mouseHold = False

    # generate houses
    houses = []
    for h in range(NHOUSES):
        houses.append(makeRandomHouse(houses))
    
    # generate persons
    persons = []
    for p in range(0, NPEOPLE):
        persons.append(makeRandomPerson(persons, houses))

    # set title
    pygame.display.set_caption('City simulation')

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

            # left click
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mousex, mousey = event.pos
                mouseHold = True
                SELX, SELY = mousex, mousey

            # left click release
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos
                for p in persons:
                    if SELBOX.colliderect(p.getRect()):
                        p.setMarked(True)
                    else:
                        p.setMarked(False)
                mouseHold = False

            # right click release
            elif event.type == MOUSEBUTTONUP and event.button == 3:
                for p in persons:
                    if p.getMarked():
                        mousex, mousey = event.pos
                        p.setTo(mousex, mousey)

            # check mouse
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

        # draw houses
        for h in houses:
            h.draw()

        # control and draw persons
        for p in persons:
            p.go(persons, houses)
            p.isBored()
            p.draw()

        # generate and draw selection box
        if mouseHold == True:
            SELBOX = selBox(SELX, SELY, mousex, mousey)

        # update frame
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def selBox(x1, y1, x2, y2):
    # selection box
    SELBOX = pygame.draw.rect(DISPLAYSURF, SELCOL, (x1, y1, x2-x1, y2-y1), 1)
    return SELBOX

        
class Person(object):
    skincol = 0
    clothescol = 0
    rect = 0
    marked = False
    tox = 0
    toy = 0
    speed = 0
    topspeed = 5
    acc = 0.1
    xpos = 0
    ypos = 0
    boredtime = 5
    boredcount = 0
    
    def __init__(self, height, width, skincol, clothescol, xpos, ypos, boredtime, topspeed):
        self.rect = pygame.Rect(xpos, ypos, width, height)
        self.skincol, self.clothescol = skincol, clothescol
        self.tox, self.toy = self.rect.centerx, self.rect.centery
        self.xpos, self.ypos = self.rect.centerx, self.rect.centery
        self.boredtime = boredtime
        self.topspeed = topspeed

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.clothescol, (self.rect))
        face = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height/3)
        pygame.draw.rect(DISPLAYSURF, self.skincol, (face))
        if self.marked == True:
            pygame.draw.rect(DISPLAYSURF, SELCOL, (self.rect), 1)

    def setMarked(self, marked):
        self.marked = marked

    def getMarked(self):
        return self.marked

    def getRect(self):
        return self.rect

    def go(self, persons, houses):
        dirx = self.tox-self.xpos
        diry = self.toy-self.ypos
        len = (dirx**2 + diry**2)**0.5
        dx = 0
        dy = 0
        collidex = False
        collidey = False
        
        # if moving
        if abs(len) > 0:
            x, y = self.xpos, self.ypos
            self.speed = self.speed + self.acc
            if self.speed > self.topspeed:
                self.speed = self.topspeed
            dx = dirx/len*self.speed
            dy = diry/len*self.speed
            if abs(dx) > abs(dirx):
                dx = dirx
                self.speed = 0
            if abs(dy) > abs(diry):
                dy = diry
                self.speed = 0
            if self.xpos != self.tox:
                x = self.xpos+dx
            if self.ypos != self.toy:
                y = self.ypos+dy

            # x axis test
            newrect=pygame.Rect(x-self.rect.width/2, self.ypos-self.rect.height/2, self.rect.width, self.rect.height)
            for p in persons:
                if p != self and newrect.colliderect(p.getRect()):
                    self.speed = self.topspeed/2
                    collidex = True
            for h in houses:
                if newrect.colliderect(h.getRect()):
                    self.speed = self.topspeed/2
                    collidex = True
            if not collidex:
                self.xpos = x
                self.rect = newrect
                self.boredcount=0

            # y axis test
            newrect=pygame.Rect(self.xpos-self.rect.width/2, y-self.rect.height/2, self.rect.width, self.rect.height)
            for p in persons:
                if p != self and newrect.colliderect(p.getRect()):
                    self.speed = self.topspeed/2
                    collidey = True
            for h in houses:
                if newrect.colliderect(h.getRect()):
                    self.speed = self.topspeed/2
                    collidey = True
            if not collidey:
                self.ypos = y
                self.rect = newrect
                self.boredcount=0

        # if not moving
        if collidex and collidey or len == 0:
            self.boredcount = self.boredcount+1/FPS

    def isBored(self):
        if self.boredcount > self.boredtime:
            self.goRandom()
        elif self.boredcount > 2:
            self.tox = self.xpos = self.rect.centerx
            self.toy = self.ypos = self.rect.centery
            self.speed = 0

    def goRandom(self):
        self.tox = random.randrange(self.rect.centerx - 50, self.rect.centerx + 50, 1)
        self.toy = random.randrange(self.rect.centery - 50, self.rect.centery + 50, 1)
        self.boredcount=0

    def setRandomPos(self):
        self.tox = self.xpos = self.rect.centerx = random.randrange(BORDER*2, WINDOWWIDTH, 1)-BORDER
        self.toy = self.ypos = self.rect.centery = random.randrange(BORDER*2, WINDOWHEIGHT, 1)-BORDER
                
    def setTo(self, x, y):
        self.tox, self.toy = x, y

class House(object):

    floors = 1
    rooms = 1
    rect = 0
    color = 0
    border = 50
    plan = 0

    def __init__(self, floors, rooms, color, x, y, plan):
        self.rect = pygame.Rect(x, y, rooms*ROOMSIZE, floors*FLOORSIZE)
        self.color, self.floors, self.rooms, self.plan = color, floors, rooms, plan

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
        y = self.rect.top
        for f in self.plan:
            x = self.rect.left
            for r in f:
                if r == 'W':
                    pygame.draw.rect(DISPLAYSURF, WINDOW, (x+ROOMSIZE/3, y+5, ROOMSIZE/3, FLOORSIZE/2-5))
                x += ROOMSIZE
            y += FLOORSIZE
                
            
        #pygame.draw.rect(DISPLAYSURF, WINDOW, (self.rect.left+ROOMSIZE/3, self.rect.top+5, ROOMSIZE/3, FLOORSIZE/2-5))
        

    def setRandomPos(self):
        x = random.randrange(BORDER*2, WINDOWWIDTH, 1)-BORDER
        y = random.randrange(BORDER*2, WINDOWHEIGHT, 1)-BORDER
        self.rect = pygame.Rect(x-self.rooms*ROOMSIZE/2, y-self.floors*FLOORSIZE/2, self.rooms*ROOMSIZE, self.floors*FLOORSIZE)

    def getRect(self):
        return self.rect

    def getArea(self):
        x = self.rect.left-self.border
        y = self.rect.top-self.border
        width = self.rect.width+2*self.border
        height = self.rect.height+2*self.border 
        area = pygame.Rect(x, y, width, height)
        return area
        
def makePerson(height, width, skincol, clothescol, xpos, ypos, boredtime, topspeed):
    person = Person(height, width, skincol, clothescol, xpos, ypos, boredtime, topspeed)
    return person

def makeHouse(floors, rooms, color, x, y, plan):
    house = House(floors, rooms, color, x, y, plan)
    return house

def makeRandomPerson(persons, houses):
    randomx = random.randrange(BORDER*2, WINDOWWIDTH, 1)-BORDER
    randomy = random.randrange(BORDER*2, WINDOWHEIGHT, 1)-BORDER
    height = random.randrange(10, 20, 1)
    width = random.randrange(4, 10, 1)
    skincol = random.choice(SKINCOLORS)
    clothescol = random.choice(CLOTHESCOLORS)
    boredtime = random.uniform(4, 10)
    topspeed = random.uniform(2, 5)
    person = Person(height, width, skincol, clothescol, randomx, randomy, boredtime, topspeed)
    collide = True
    while collide == True:
        collide = False
        for p in persons:
            if person.getRect().colliderect(p.getRect()):
                person.setRandomPos()
                collide = True
        for h in houses:
            if person.getRect().colliderect(h.getRect()):
                person.setRandomPos()
                collide = True
    return person

def makeRandomHouse(houses):
    randomx = random.randrange(BORDER*2, WINDOWWIDTH, 1)-BORDER
    randomy = random.randrange(BORDER*2, WINDOWHEIGHT, 1)-BORDER
    floors = random.randrange(1, 4, 1)
    rooms = random.randrange(1, 4, 1)
    color = random.choice(HOUSECOLORS)
    plan = makeFloorplan(floors, rooms)
    house = makeHouse(floors, rooms, color, randomx, randomy, plan)
    collide = True
    while collide == True:
        collide = False
        for h in houses:
            if house.getRect().colliderect(h.getArea()):
                house.setRandomPos()
                collide = True
    return house

def makeFloorplan(floors, rooms):
    options = (' ', 'W')
    plan = []
    for f in range(floors):
        plan.append([random.choice(options) for r in range(rooms)])
    return plan

if __name__ == '__main__':
    main()
