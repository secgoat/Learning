from RLCONSTANTS import *
import RLobject
import RLpanel
#import pygame
#from pygame.locals import *
#import random

#Map Constants
MWIDTH = 512
MHEIGHT = 384
ROOMMAX = 160
ROOMMIN = 96
MAXROOMS = 10

#colors


class Room:
    def __init__(self, rect, explored = False, connected = False):
        self.rect = rect
        self.explored = explored
        self.connected = connected
        
    def createRoom(self, room, gameMap):
        gameMap.append(room)       
        return gameMap      
    
class Map:
    def __init__(self):
        self.level_map = []
        self.floors = []
        self.walls = []
        self.items = []
        self.mobs = []
        self.images = {}
        self.makeMap()
        self.populateLevel()
         
         
    def makeMap(self):
        self.level_map = [
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        for a in range(len(self.level_map)):
            for b in range(len(self.level_map[a])):
                if self.level_map[a][b] == 1:
                    y = a * IMGSIZE
                    x = b * IMGSIZE
                    self.walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                
        for a in range(len(self.level_map)):
            for b in range(len(self.level_map[a])):
                if self.level_map[a][b] == 0:
                    y = a * IMGSIZE
                    x = b * IMGSIZE
                    self.floors.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE)) 
    

    def populateLevel(self):
        for x in range(len(self.floors)):
            if random.randint(0,10) <= 1:
                if random.randint(0,2) == 0:
                    item = RLobject.Object('whip.bmp', self.floors[x].top, self.floors[x].left)
                    item.kind = 'whip'
                else:
                    item = RLobject.Object('gem.bmp', self.floors[x].top, self.floors[x].left)
                    item.kind = 'gem'
                self.items.append(item)
        self.addMobs()
    
    def addMobs(self):
        for x in range(len(self.floors)):
            if random.randint(0,10) <= 1:
                mob = RLobject.Mob('bat.bmp', self.floors[x].top, self.floors[x].left)
        self.mobs.append(mob) 


def renderAll(font, surface, testMap, images, player):
    
    surface.fill((0,0,0))
    RLpanel.update(player, font)

    for a in range(len(testMap.level_map)):
        for b in range(len(testMap.level_map[a])):
            y = a * IMGSIZE # this sets the x and y coords by the number of pixels the image is, 16 ,32 etc.
            x = b * IMGSIZE
            if testMap.level_map[a][b] == 0 or testMap.level_map[a][b] == 9:
                surface.blit(images['floor'], (x, y))
            elif testMap.level_map[a][b] == 1:
                surface.blit(images['wall'], (x, y))    
    #draw all objects in the list
    for object in testMap.items:
        object.draw(surface)
    for mob in testMap.mobs:
        mob.draw(surface)
    player.draw(surface)
    if player.whipping == True:
        player.whip(surface, player.rect)
    pygame.display.update() 