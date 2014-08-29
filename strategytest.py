import pygame, sys, math, random
from pygame.locals import *

level = [
    "1WWWWWWWWWWWWWWW",
    "2WBBBBBBBBBBBBBW",
    "3WB  MMMMM    BW",
    "4WB  WWWWM    BW",
    "5WB  WWW     BBW",
    "6WB  W       BWW",
    "7WB  W       BWW",
    "8WB  W       BBW",
    "9WB  WWW      BW",
    "0WB    W      BW",
    "1WB MM W      BW",
    "2WB MM W      BW",
    "3WB   BWB    BBW",
    "4WBBBBBWBBBBBBWW",
    "5WWWWWWWWWWWWWWW",
    ]

# framerate
FPS = 30


BGCOLOR = (0,0,0)
RED = (255,0,0)
RED2 = (255,30,30)
RED3 = (255,60,60)
GREEN = (0,255,0)
DARKGREEN = (0,128,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,128)
BEACH = (255,255,128)
DARKBEACH = (128,128,64)
BROWN1 = (139,69,19)
BROWN2 = (160,82,45)
BROWN3 = (205,133,63)
BROWN4 = (222,184,135)
WHITE = (255,255,255)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    SCALE = 60
    VIEWANGLE = math.pi/3

    # window
    UX = SCALE/2
    UY = math.sin(VIEWANGLE)*SCALE/2
    UZ = math.cos(VIEWANGLE)*SCALE/2
    WINDOWWIDTH = round((len(level)+2)*2*UX)
    WINDOWHEIGHT = round((len(level)+2)*2*UY)
    XTOP = WINDOWWIDTH/2
    YTOP = WINDOWHEIGHT/2-(len(level)+15)/2*UY
    reds = []

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    startscale = SCALE
    startangle = VIEWANGLE
    for t in range(FPS*2):
        SCALE = (t*startscale+1)/(FPS*2)
        VIEWANGLE = (t*startangle+1)/(FPS*2)
        UX, UY, UZ, YTOP = updateView(SCALE,VIEWANGLE,WINDOWHEIGHT)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid(XTOP,YTOP,UX,UY,UZ,0,0)        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    while True:

        mouseClicked = False
        # check input events
        for event in pygame.event.get():

            # quit
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYUP and event.key == K_2:
                VIEWANGLE += 0.1
                print('view plus')

            elif event.type == KEYUP and event.key == K_1:
                VIEWANGLE -= 0.1
                print('view minus')

            elif event.type == KEYUP and event.key == K_x:
                SCALE = SCALE*1.5
                print('zoom in')

            elif event.type == KEYUP and event.key == K_z:
                SCALE = SCALE/1.5
                print('zoom out')

            # left click release
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                mouseClicked = True
                
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                

        # draw background
        UX, UY, UZ, YTOP = updateView(SCALE,VIEWANGLE,WINDOWHEIGHT)
        DISPLAYSURF.fill(BGCOLOR)
        s = drawGrid(XTOP,YTOP,UX,UY,UZ,mousex,mousey)
        if mouseClicked:
            reds.append(s)
        for r in reds:
            #drawRed(r)
            drawCube(r, UX, UY, UZ)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawGrid(XTOP,YTOP, UX, UY, UZ, mousex, mousey):

    x = XTOP
    y = YTOP
    squares = []
    for row in level:
        for col in row:
            if col == "W":
                squares.append(drawWater(x,y,UX,UY))
            elif col == " ":
                squares.append(drawGround(x,y,UX,UY))
            elif col == "B":
                squares.append(drawBeach(x,y,UX,UY))
            elif col == "M":
                squares.append(drawMountain(x,y,UX,UY,UZ))
            x += UX
            y += UY
        y = YTOP + UY*(level.index(row)+1)
        x = XTOP - UX*(level.index(row)+1)
    for s in squares:
        if point_in_poly(mousex, mousey, s):
            pygame.draw.polygon(DISPLAYSURF, WHITE, s, 5)
            return s

def drawWater(x,y,UX,UY):
    pointlist = []
    pointlist.append((x,y))
    pointlist.append((x+UX,y+UY))
    pointlist.append((x,y+2*UY))
    pointlist.append((x-UX,y+UY))
    pygame.draw.polygon(DISPLAYSURF, BLUE, pointlist)
    pygame.draw.polygon(DISPLAYSURF, DARKBLUE, pointlist, 1)
    return pointlist

def drawGround(x,y,UX,UY):
    pointlist = []
    pointlist.append((x,y))
    pointlist.append((x+UX,y+UY))
    pointlist.append((x,y+2*UY))
    pointlist.append((x-UX,y+UY))
    pygame.draw.polygon(DISPLAYSURF, GREEN, pointlist)
    pygame.draw.polygon(DISPLAYSURF, DARKGREEN, pointlist, 1)
    return pointlist

def drawBeach(x,y,UX,UY):
    pointlist = []
    pointlist.append((x,y))
    pointlist.append((x+UX,y+UY))
    pointlist.append((x,y+2*UY))
    pointlist.append((x-UX,y+UY))
    pygame.draw.polygon(DISPLAYSURF, BEACH, pointlist)
    pygame.draw.polygon(DISPLAYSURF, DARKBEACH, pointlist, 1)
    return pointlist

def drawMountain(x,y,UX,UY,UZ):
    n,e,s,w,c = (x,y),(x+UX,y+UY),(x,y+2*UY),(x-UX,y+UY),(x,y+UY-UZ)
    NW = (n,w,c)
    NE = (n,e,c)
    SW = (s,w,c)
    SE = (s,e,c)
    pygame.draw.polygon(DISPLAYSURF, BROWN3, NE)
    pygame.draw.polygon(DISPLAYSURF, BROWN1, NW)
    pygame.draw.polygon(DISPLAYSURF, BROWN4, SE)
    pygame.draw.polygon(DISPLAYSURF, BROWN2, SW)
    pointlist = (n,e,s,w)
    return pointlist

def updateView(SCALE,VIEWANGLE,WINDOWHEIGHT):
    UX = SCALE/2
    UY = math.sin(VIEWANGLE)*SCALE/2
    UZ = math.cos(VIEWANGLE)*SCALE/2
    YTOP = WINDOWHEIGHT/2-len(level)*UY
    return UX, UY, UZ, YTOP

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def drawRed(pointlist):
    pygame.draw.polygon(DISPLAYSURF, RED, pointlist, 3)

def drawCube(pointlist, UX, UY, UZ):
    UX, UY, UZ = UX/2, UY/2, UZ/2
    xdown, ydown = pointlist[2]
    bsy = (ydown - UY)
    bsx = xdown
    bs = (bsx, bsy)
    bw = (bsx-UX, bsy -UY)
    be = (bsx+UX, bsy-UY)
    ts = (bsx, bsy- UZ)
    tn = (bsx, bsy-2*UY-UZ)
    tw = (bsx-UX, bsy -UY -UZ)
    te = (bsx+UX, bsy-UY-UZ)
    pygame.draw.polygon(DISPLAYSURF, RED, (bs,bw,tw,ts))
    pygame.draw.polygon(DISPLAYSURF, RED2, (bs,be,te,ts))
    pygame.draw.polygon(DISPLAYSURF, RED3, (ts,tw,tn,te))
    
    
if __name__ == '__main__':
    main()
