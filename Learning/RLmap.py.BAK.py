import pygame
from pygame.locals import *

MWIDTH = 1000
MHEIGHT = 1000

#colors
DARK_WALL = (0,0,100)
DARK_GROUND = (50,50,150)

class MapRect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        
class Tile:
    #a tile on the map and it's properties
    def __init__(self, blocked, blockedSight = None):
        self.blocked = blocked
        #by default if a tile is blocked it also blocks sight
        if blockedSight == None: blockedSight = blocked
        self.blockedSight = blockedSight
        self.tileRect = [0,0,0,0]
        
def createRoom(room, gameMap):
        for x in range(room.x1 +1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                gameMap[x][y].blocked = False
                gameMap[x][y].blockedSight = False
        return gameMap      
def hTunnel(x1, x2, y, gameMap):
    for x in range(min(x1,x2), max(x1,x2) +1):
        gameMap[x][y].blocked = False
        gameMap[x][y].blockedSight = False
    return gameMap

def vTunnel(y1, y2, x, gameMap):
    for y in range(min(y1,y2), max(y1,y2) +1):
        gameMap[x][y].blocked = False
        gameMap[x][y].blockedSight = False
    return gameMap

def makeMap():
    #fill the map with unblocked tiles
    gameMap = [[Tile(True) for y in range(MHEIGHT)] for x in range(MWIDTH)]
    #gameMap[30][22].blocked = True
    #gameMap[30][22].blockedSight = True
    #gameMap[60][22].blocked = True
    #gameMap[60][22].blockedSight = True
    room1 = Rect(200, 150, 100, 150)
    room2 = MapRect(500, 150, 100, 150)
    gameMap = createRoom(room1, gameMap)
    gamemap = createRoom(room2, gameMap)
    gameMap = hTunnel(250, 550, 230, gameMap)
    return gameMap

def renderAll(font, surface, objects, walls, gameMap):
    surface.fill((0,0,0))
    for y in range(MHEIGHT):
        for x in range(MWIDTH):
            
            if gameMap[x][y].blockedSight == True: 
                wallIcon = font.render('W', True, DARK_WALL)
                gameMap[x][y].tileRect = wallIcon.get_rect()
                gameMap[x][y].tileRect.left = x
                gameMap[x][y].tileRect.top = y
                walls.append(gameMap[x][y].tileRect)
                surface.blit(wallIcon, (x,y))
            else:
                floorIcon = font.render('F', True, DARK_GROUND)
                surface.blit(floorIcon, (x,y))
    #draw all objects in the list
    for object in objects:
        object.draw(font, surface) 
    pygame.display.update()