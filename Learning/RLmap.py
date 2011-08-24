
from RLCONSTANTS import *
import RLobject
import RLpanel
from RLlevels import *
#import pygame
#from pygame.locals import *
#import random

#level map width and height set by which map is loaded later
map_width = 0
map_height = 0

#view port size, what part of the map is shown on the screen at any given time.


class Tile():
    def __init__(self, rect, explored = False):
        self.rect = rect
        self.explored = explored
        self.connected = connected
        
    def createRoom(self, room, gameMap):
        gameMap.append(room)       
        return gameMap      
    
class Map:
    def __init__(self):
        self.level = 1
        self.level_map = []
        self.floors = []
        self.walls = []
        self.doors = []
        self.items = []
        self.mobs = []
        self.images = {}
        self.makeMap()
        #self.populateLevel()
         
         
    def makeMap(self):
        self.level_map = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,20,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,20,0,0,0,0,40,0,0,0,0,20,0,0,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,1],
  [1,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,40,0,0,0,20,0,0,0,40,0,0,0,1],
  [1,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
  [1,0,0,0,0,0,0,0,1,1,44,42,44,42,44,1,1,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,40,0,0,20,0,1,1,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,1,1,20,0,1],
  [1,0,0,0,0,40,0,0,1,1,42,44,42,44,42,1,1,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1],
  [1,0,0,20,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,40,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,2,2,1,1,0,40,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,1,1,8,8,8,8,8,8,8,8,8,8,8,8,8,0,43,1,1,1,0,0,2,58,1,1,0,0,1],
  [1,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,2,2,1,1,40,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1],
  [1,1,1,1,1,1,0,20,0,0,0,0,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,41,1,1,20,0,0,0,1,1,0,20,1],
  [1,45,1,1,1,1,0,0,0,0,0,0,0,18,3,3,3,3,3,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,41,1,1,0,0,0,20,1,1,0,0,1],
  [1,1,0,1,1,1,0,0,0,0,0,0,0,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,41,1,1,20,0,0,0,1,1,0,40,1],
  [1,1,1,0,1,1,0,20,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,20,0,0,40,1,1,41,1,1,0,20,0,0,1,1,0,0,1],
  [1,1,0,1,1,1,0,0,0,0,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,0,0,0,0,0,0,0,1,1,41,1,1,0,0,0,20,1,1,40,0,1],
  [1,1,0,1,1,1,0,0,0,0,20,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,1,1,41,1,1,20,0,0,0,1,1,0,0,1],
  [1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,4,1,1,0,0,0,0,0,40,0,0,1,1,41,1,1,0,0,20,0,1,1,20,0,1],
  [1,2,2,2,1,1,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,20,0,1,1,0,0,0,0,0,1,1,20,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,40,0,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,20,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,0,20,1,1,0,0,0,0,0,0,20,0,0,0,40,0,0,20,0,18,0,19,19,1],
  [1,2,2,2,2,2,2,2,1,1,42,0,0,1,1,0,0,0,0,0,0,20,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,2,2,2,2,2,2,2,1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,20,0,1,1,1,1,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,41,41,41,41,41,41,41,1,1,43,43,0,0,0,20,0,0,0,1,1,0,0,40,0,0,1,1,20,20,20,20,20,1,1,0,0,0,0,0,0,59,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        for a in range(len(self.level_map)):       
            for b in range(len(self.level_map[a])):
                y = a * IMGSIZE
                x = b * IMGSIZE
                if self.level_map[a][b] == 0:
                    self.floors.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                if self.level_map[a][b] >= 1 and self.level_map[a][b] <= 3:  
                    self.walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                if self.level_map[a][b] == 4:
                    door = RLobject.Door('door.bmp', x, y)
                    self.doors.append(door)
                if self.level_map[a][b] == 20:
                    mob = RLobject.Mob('a.bmp', x , y)
                    self.mobs.append(mob)
                if self.level_map[a][b] == 40:
                    item = RLobject.Object('gem.bmp', x, y, 'gem')
                    self.items.append(item)
                if self.level_map[a][b] == 41:
                    item = RLobject.Object('whip.bmp', x , y, 'whip')
                    self.items.append(item)
                if self.level_map[a][b] == 42:
                    item = RLobject.Object('teleport.bmp', x , y, 'teleport')
                    self.items.append(item)
                if self.level_map[a][b] == 43:
                    item = RLobject.Object('key.bmp', x , y, 'key')
                    self.items.append(item)
                if self.level_map[a][b] == 44:
                    item = RLobject.Object('gold.bmp', x , y, 'gold')
                    self.items.append(item)
                if self.level_map[a][b] == 45:
                    item = RLobject.Object('chest.bmp', x , y, 'chest')
                    self.items.append(item)
        map_width = b * IMGSIZE
        map_height = a * IMGSIZE

    def populateLevel(self): # for randomly generated levels
        item = None
        max_items = 30
        num_items = 0
        for x in range(len(self.floors)):
            if random.randint(0,10) == 0 and num_items < max_items:
                num = random.randint(0,1)
                if num == 0:
                    item = RLobject.Object('whip.bmp', self.floors[x].top, self.floors[x].left)
                    item.kind = 'whip'
                    num_items += 1
                    #print(item.kind)
                    #print(item.rect)
                elif num == 1:
                    item = RLobject.Object('gem.bmp', self.floors[x].top, self.floors[x].left)
                    item.kind = 'gem'
                    num_items +=1
                    #print(item.kind)
                    #print(item.rect)
                self.items.append(item)
            else:
                pass

def renderAll(font, surface, testMap, images, player):
    
    surface.fill((0,0,0))
    RLpanel.update(player, font)
    #mapSurface = surface.subsurface((corner_x,0) +(view_width, view_height))
    for a in range(len(testMap.level_map)):
        for b in range(len(testMap.level_map[a])):
    #for a in range(int(view_width / IMGSIZE)): # a=y b = x
        #for b in range(int(view_height / IMGSIZE)):
            y = a * IMGSIZE # this sets the x and y coords by the number of pixels the image is, 16 ,32 etc.
            x = b * IMGSIZE
            surface.blit(images['floor'], (x,y))
            if testMap.level_map[a][b] == 0:
                surface.blit(images['floor'], (x, y))
            elif testMap.level_map[a][b] == 1:
                surface.blit(images['wall'], (x, y))
            elif testMap.level_map[a][b] == 2:
                surface.blit(images['breakable'], (x,y))
            elif testMap.level_map[a][b] == 3:
                surface.blit(images['water'], (x, y))
            elif testMap.level_map[a][b] == 19:
                surface.blit(images['stairs'], (x,y))
            
    #draw all objects in the list
    for object in testMap.items:
        object.draw(surface)
    for mob in testMap.mobs:
        mob.draw(surface)
    for door in testMap.doors:
        door.draw(surface)
    player.draw(surface)
    if player.whipping == True:
        player.whip(surface)
    pygame.display.update() 