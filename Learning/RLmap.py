
from RLCONSTANTS import *
import RLobject
import RLpanel
import RLlevels
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
    def __init__(self, level, player):
        self.level = level
        self.level_map = []
        self.panel = RLpanel.Panel()
        self.floors = []
        self.exits = []
        self.walls = []
        self.hidden_walls = []
        self.breakable = []
        self.doors = []
        self.items = []
        self.mobs = []
        self.images = {}
        self.makeMap(player)
        #self.populateLevel()
         
    def clearLevel(self):
        self.level_map = []
        self.floors = []
        self.exits = []
        self.walls = []
        self.hidden_walls = []
        self.breakable = []
        self.doors = []
        self.items = []
        self.mobs = []
        
    def makeMap(self, player):
        f = open('lvl{}.txt'.format(self.level),'r')
        lines = f.readlines()
        self.level_map = lines
        
        for a in range(len(self.level_map)):
            for b in range(len(self.level_map[a])):
                y = a * IMGSIZE
                x = b * IMGSIZE
                if self.level_map[a][b] == ' ':
                    self.floors.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                if self.level_map[a][b] == '#' or self.level_map[a][b] == '6' or self.level_map[a][b] == 'R':  
                    self.walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                if self.level_map[a][b] == 'X' or self.level_map[a][b] == 'Y':
                    breakable_wall = RLobject.Object('breakable.bmp', x, y)
                    self.breakable.append(breakable_wall)
                if self.level_map[a][b] == 'D':
                    door = RLobject.Door('door.bmp', x, y)
                    self.doors.append(door)
                
                if self.level_map[a][b] == 'P':
                    player.rect.top = a * IMGSIZE
                    player.rect.left = b * IMGSIZE
                    
                if self.level_map[a][b] == ':':
                    self.hidden_walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                if self.level_map[a][b] == '1':
                    mob = RLobject.Mob('gnome.bmp', x , y)
                    self.mobs.append(mob)
                if self.level_map[a][b] == '2':
                    mob = RLobject.Mob('elf_mummy.bmp', x , y)
                    self.mobs.append(mob)
                if self.level_map[a][b] == '3':
                    mob = RLobject.Mob('ogre_lord.bmp', x , y)
                    self.mobs.append(mob)
                if self.level_map[a][b] == '4':
                    mob = RLobject.Mob('umber_hulk.bmp', x , y)
                    self.mobs.append(mob)
                
                if self.level_map[a][b] == '+':
                    item = RLobject.Object('gem.bmp', x, y, 'gem')
                    self.items.append(item)
                if self.level_map[a][b] == 'W':
                    item = RLobject.Object('whip.bmp', x , y, 'whip')
                    self.items.append(item)
                if self.level_map[a][b] == 'T':
                    item = RLobject.Object('teleport.bmp', x , y, 'teleport')
                    self.items.append(item)
                if self.level_map[a][b] == 'K':
                    item = RLobject.Object('key.bmp', x , y, 'key')
                    self.items.append(item)
                if self.level_map[a][b] == '*':
                    item = RLobject.Object('gold.bmp', x , y, 'gold')
                    self.items.append(item)
                if self.level_map[a][b] == 'C':
                    item = RLobject.Object('chest.bmp', x , y, 'chest')
                    self.items.append(item)
                if self.level_map[a][b] == 'L':
                    self.exits.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))

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
                elif num == 1:
                    item = RLobject.Object('gem.bmp', self.floors[x].top, self.floors[x].left)
                    item.kind = 'gem'
                    num_items +=1
                self.items.append(item)
            else:
                pass

def renderAll(font, surface, testMap, images, player):
    surface.fill((0,0,0))
    testMap.panel.update(player, font)
    
    
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
            #elif testMap.level_map[a][b] == '#' or testMap.level_map[a][b] == '6':
                #surface.blit(images['wall'], (x, y))
            elif testMap.level_map[a][b] == 'R':
                surface.blit(images['water'], (x, y))
            elif testMap.level_map[a][b] == 'L':
                surface.blit(images['stairs'], (x,y))
            
            
    #draw all objects in the lists
    for wall in testMap.walls:
        surface.blit(images['wall'], wall)
    for object in testMap.items:
        object.draw(surface)
    for mob in testMap.mobs:
        mob.draw(surface)
    for door in testMap.doors:
        door.draw(surface)
    for breakable_wall in testMap.breakable:
        breakable_wall.draw(surface)
    player.draw(surface)
    if player.whipping == True:
        player.whip(surface, testMap)
        
    for a in range(len(testMap.level_map)):
        for b in range(len(testMap.level_map[a])):
            if testMap.level_map[a][b] == 'R':
                surface.blit(images['water'], (x, y))
        
    pygame.display.update() 