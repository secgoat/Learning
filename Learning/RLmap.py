import os
from RLCONSTANTS import *
import RLobject
import RLpanel
import RLlevels
import pygame
from pygame.locals import *
import random


#level map width and height set by which map is loaded later
map_width = 0
map_height = 0

#view port size, what part of the map is shown on the screen at any given time.

class Tile():
    def __init__(self, x,y, triggered = False, kind = None):
        self.rect = pygame.Rect(x,y,IMGSIZE,IMGSIZE)
        self.triggered = triggered
        self.attached = [] # list of tiles that are affected when this tile is triggered
        self.kind = kind #kinds: extra gems revealed, extra monsters added, remove walls, add walls,

    def trigger(self, game):
        level_map = game.level_map 
        if self.triggered == False:
            if self.kind == 'gems':
                level_map.panel.messages.append('You set of a Reveal Gems Spell.')
                new_gems = random.randint(1,6)
                for x in range(new_gems):
                    random_space = random.randint(1, len(level_map.floors))
                    random_space = level_map.floors.pop(random_space)
                    item = RLobject.Object(os.path.join(IMGDIR, 'gem.bmp'), random_space.left, random_space.top, 'gem')
                    level_map.items.append(item)
            
            if self.kind == 'walls1':
                walls = level_map.triggered_walls['7']
                for wall in walls:
                    level_map.walls.append(wall)
                level_map.panel.messages.append('The walls are closing in on you!')
            
            if self.kind == 'walls2':
                walls = level_map.triggered_walls['8']
                for wall in walls:
                    level_map.walls.append(wall)
                level_map.panel.messages.append('The walls are closing in on you!')
            
            if self.kind == 'remove_walls':
                walls = level_map.triggered_walls['Y']
                for wall in walls:
                    game.level_map.breakable.remove(wall)
                    
            if self.kind == 'move_walls':
                #game.level_map.moveable_wall_spaces.append(self.rect)
                game.timers['move_walls'] = pygame.time.set_timer(USEREVENT+4, 1000)
            
            if self.kind == 'teleport':
                game.player.teleport(game)
                
            self.triggered = True
        else:
            return
        
   
    
class Map:
    def __init__(self, level, player):
        self.level = level
        self.level_map = []
        self.panel = RLpanel.Panel()
        self.floors = []
        self.triggers = []
        self.exits = []
        self.walls = []
        self.water = []
        self.hidden_walls = []
        self.triggered_walls = {'7':[], '8':[], 'Y':[]}
        self.breakable = []
        self.moveable_wall_spaces = []
        self.lava = []
        self.pits = []
        self.doors = []
        self.items = []
        self.mobs = []
        self.images = {}
        self.makeMap(player)
        #self.populateLevel()
         
    def clearLevel(self):
        self.floors = []
        self.triggers = []
        self.exits = []
        self.walls = []
        self.water = []
        self.hidden_walls = []
        self.triggered_walls = {'7':[], '8':[], 'Y':[]}
        self.breakable = []
        self.moveable_wall_spaces = []
        self.lava = []
        self.pits = []
        self.doors = []
        self.items = []
        self.mobs = []
    
    def moveWalls(self, game): #level4
        available_spaces = []
        player_pos = game.player.rect
        for floor in game.level_map.floors:
            if (floor.top >= (player_pos.top + IMGSIZE) and floor.top <= (player_pos.top + IMGSIZE * 4)) or (floor.top <= (player_pos.top - IMGSIZE) and floor.top <= (player_pos.top - IMGSIZE * 4)):
                available-space.append(floor)
            if (floor.left >= (player_pos.left + IMGSIZE) and floor.left <= (player_pos.left + IMGSIZE * 4)) or (floor.left <= (player_pos.left - IMGSIZE) and floor.left <= (player_pos.left - IMGSIZE * 4)):
                available-space.append(floor)
            
    def lavaFlow(self, game):
        up = ' '
        down = ''
        left = ''
        right = ''
        for lava in game.level_map.lava:
            up = lava.rect.move(-IMGSIZE,0)
            down = lava.rect.move(IMGSIZE,0)
            left = lava.rect.move(0, -IMGSIZE)
            right =  lava.rect.move(0, IMGSIZE)
            #print('up: {0}, down:{1}, left:{2}, right{3}'.format(up,down,left,right))
            if down in game.level_map.floors:
                new_lava = RLobject.Object(os.path.join(IMGDIR,'lava.bmp'), down.left, down.top)
                game.level_map.floors.remove(down)
                game.level_map.lava.append(new_lava)
                for item in game.level_map.items:
                    if item.rect == down:
                        game.level_map.items.remove(item)
                return
            if left in game.level_map.floors:
                new_lava = RLobject.Object(os.path.join(IMGDIR,'lava.bmp'), left.left, left.top)
                game.level_map.floors.remove(left)
                game.level_map.lava.append(new_lava)
                for item in game.level_map.items:
                    if item.rect == left:
                        game.level_map.items.remove(item)
                return
            if right in game.level_map.floors:
                new_lava = RLobject.Object(os.path.join(IMGDIR,'lava.bmp'), right.left, right.top)
                game.level_map.floors.remove(right)
                game.level_map.lava.append(new_lava)
                for item in game.level_map.items:
                    if item.rect == right:
                        game.level_map.items.remove(item)
                return
            if up in game.level_map.floors:
                new_lava = RLobject.Object(os.path.join(IMGDIR,'lava.bmp'), up.left, up.top)
                game.level_map.floors.remove(up)
                game.level_map.lava.append(new_lava)
                for item in game.level_map.items:
                    if item.rect == up:
                        game.level_map.items.remove(item)
                return
        for item in game.level_map.items:
            if item.rect == up or item.rect == down or item.rect ==left or item.rect == right:
                game.level_map.items.remove(item)
            
                    
    def makeMap(self, player):
        f = open(os.path.join(LVLDIR,'lvl{}.txt').format(self.level),'r')
        lines = f.readlines()
        self.level_map = lines
        walls = ['#', '7', '8', 'X', 'Y', 'D', 'R', 'M','L','V','=',]
        
        for a in range(len(self.level_map)):
            for b in range(len(self.level_map[a])):
                y = a * IMGSIZE
                x = b * IMGSIZE
#---------------Walls, floors etc-----------------------------------------------------------------------------                
                #if self.level_map[a][b] == ' ':
                if self.level_map[a][b] not in walls:
                    self.floors.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                    '''if self.level == '4':
                        floor = Tile(x,y, False, wall_spaces)
                        self.moveable_wall_spaces.append(floor)
                        self.triggers.append(floor)'''
                
                if self.level_map[a][b] == '#' or self.level_map[a][b] == '6' or self.level_map[a][b] == 'R':  
                    self.walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                
                if self.level_map[a][b] == 'X':
                    breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                    self.breakable.append(breakable_wall)
                if self.level_map[a][b] == 'Y':
                    breakable_wall =  RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                    self.triggered_walls['Y'].append(breakable_wall.rect)
                    self.breakable.append(breakable_wall)
                
                '''if self.level_map[a][b] == 'M':
                    moveable_wall = RLobject.Object(os.path.join(IMGDIR, 'breakable.bmp'), x, y)
                    self.moveable_wall.append(moveable_wall)
                    self.walls.append(moveable_wall)'''
                   
                if self.level_map[a][b] == 'M':
                    moveable_wall = RLobject.Object(os.path.join(IMGDIR, 'breakable.bmp'), x, y)
                    self.breakable.append(moveable_wall)
                        
                if self.level_map[a][b] == 'D':
                    door = RLobject.Door(os.path.join(IMGDIR,'door.bmp'), x, y)
                    self.doors.append(door)
                
                if self.level_map[a][b] == ':':
                    self.hidden_walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                
                if self.level_map[a][b] == '7':
                    wall = pygame.Rect(x,y,IMGSIZE,IMGSIZE)
                    self.triggered_walls['7'].append(wall) # uses a dictionary with a list as the value to keep track off all walls to be triggered
                
                if self.level_map[a][b] == '8':
                    wall = pygame.Rect(x,y,IMGSIZE,IMGSIZE)
                    self.triggered_walls['8'].append(wall)
                
                if self.level_map[a][b] == 'L':
                    self.exits.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))

                if self.level_map[a][b] == 'V':
                    lava = RLobject.Object(os.path.join(IMGDIR,'lava.bmp'), x, y)
                    self.lava.append(lava)
                if self.level_map[a][b] == '=':
                    pit = RLobject.Object(os.path.join(IMGDIR,'pit.bmp'), x, y)
                    self.pits.append(pit)
                if self.level_map[a][b] == 'R':
                    water = pygame.Rect(x,y,IMGSIZE,IMGSIZE)
                    self.water.append(water)
#----------------Player------------------------------------------------------------------------------------------                
                if self.level_map[a][b] == 'P':
                    player.rect.top = y
                    player.rect.left = x
                    
#-----------------MOBS-------------------------------------------------------------------------------                
                if self.level_map[a][b] == '1':
                    mob = RLobject.Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y)
                    self.mobs.append(mob)
                
                if self.level_map[a][b] == '2':
                    mob = RLobject.Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y)
                    self.mobs.append(mob)
                
                if self.level_map[a][b] == '3':
                    mob = RLobject.Mob(os.path.join(IMGDIR,'ogre_lord.bmp'), x , y)
                    self.mobs.append(mob)
                
                if self.level_map[a][b] == '4':
                    mob = RLobject.Mob(os.path.join(IMGDIR,'umber_hulk.bmp'), x , y)
                    self.mobs.append(mob)
#---------------Items-----------------------------------------------------------------                
                if self.level_map[a][b] == '+':
                    item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                    self.items.append(item)
                
                if self.level_map[a][b] == 'W':
                    item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                    self.items.append(item)
                
                if self.level_map[a][b] == 'T':
                    item = RLobject.Object(os.path.join(IMGDIR,'teleport.bmp'), x , y, 'teleport')
                    self.items.append(item)
                
                if self.level_map[a][b] == 'K':
                    item = RLobject.Object(os.path.join(IMGDIR,'key.bmp'), x , y, 'key')
                    self.items.append(item)
                
                if self.level_map[a][b] == '*':
                    item = RLobject.Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                    self.items.append(item)
                
                if self.level_map[a][b] == 'C':
                    item = RLobject.Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
                    self.items.append(item)

                if self.level_map[a][b] == 'Q':
                    item = RLobject.Object(os.path.join(IMGDIR,'ring.bmp'),x,y,'whip_ring')
                    self.items.append(item)
#---------------Map Triggers-------------------------------------------------------------                    
                if self.level_map[a][b] == 'H':
                    trigger = Tile(x, y, False, 'gems')
                    self.triggers.append(trigger)
                
                if self.level_map[a][b] == '`':
                    trigger = Tile(x, y, False, 'walls1') #reveal hidden walls labeled as 7 on map
                    self.triggers.append(trigger)
                
                if self.level_map[a][b] == ',':
                    trigger = Tile(x, y, False, 'walls2') #reveal hidden walls labeled as 8 on map.
                    self.triggers.append(trigger)
                if self.level_map[a][b] == '~':
                    trigger = Tile(x, y, False, 'remove_walls')
                    self.triggers.append(trigger)
                
                if self.level_map[a][b] == '.':
                    item = RLobject.Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                    trigger = Tile(x,y, False, 'teleport')
                    self.triggers.append(trigger)
                    self.items.append(item)
                if self.level_map[a][b] == 'A':
                    trigger = Tile(x,y, False, 'move_walls')
                    self.triggers.append(trigger)
        self.panel.messages.append('Press any key to start level')
        
    
    def populateLevel(self): # for randomly generated levels
        item = None
        max_items = 30
        num_items = 0
        for x in range(len(self.floors)):
            if random.randint(0,10) == 0 and num_items < max_items:
                num = random.randint(0,1)
                if num == 0:
                    item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), self.floors[x].top, self.floors[x].left)
                    item.kind = 'whip'
                    num_items += 1
                elif num == 1:
                    item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), self.floors[x].top, self.floors[x].left)
                    item.kind = 'gem'
                    num_items +=1
                self.items.append(item)
            else:
                pass

def renderAll(font, surface, testMap, images, player):
    surface.fill((0,0,0))

    testMap.panel.update(player, font, testMap)
    
    
    #mapSurface = surface.subsurface((corner_x,0) +(view_width, view_height))
    for a in range(len(testMap.level_map)):
        for b in range(len(testMap.level_map[a])):
    #for a in range(int(view_width / IMGSIZE)): # a=y b = x
        #for b in range(int(view_height / IMGSIZE)):
            y = a * IMGSIZE # this sets the x and y coords by the number of pixels the image is, 16 ,32 etc.
            x = b * IMGSIZE
            surface.blit(images['floor'], (x,y))
            #if testMap.level_map[a][b] == ' ':
                # surface.blit(images['floor'], (x,y))
           # elif testMap.level_map[a][b] == 'L':
                #surface.blit(images['stairs'], (x,y))          
            
    #draw all objects in the lists
    for wall in testMap.walls:
        surface.blit(images['wall'], wall)
    for water in testMap.water:
        surface.blit(images['water'], water)
    for exit in testMap.exits:
        surface.blit(images['stairs'], exit)
    for object in testMap.items:
        object.draw(surface)
    for mob in testMap.mobs:
        mob.draw(surface)
    for door in testMap.doors:
        door.draw(surface)
    for breakable_wall in testMap.breakable:
        breakable_wall.draw(surface)
    for lava in testMap.lava:
        #print(len(testMap.lava))
        lava.draw(surface)
    for pit in testMap.pits:
        pit.draw(surface)
    #for wall in testMap.moveable_wall:
       #wall.draw(surface)
    player.draw(surface)
    if player.whipping == True:
        player.whip(surface, testMap)
        
        
    pygame.display.update() 