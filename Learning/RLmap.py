import os
from RLCONSTANTS import *
import RLobject
import RLpanel
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
                level_map.triggered_walls['Y'] = []
            
            if self.kind == 'teleport':
                game.player.teleport(game)
                
            self.triggered = True
        else:
            return

class Map:
    def __init__(self, level, game):
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
        self.moveable_walls = []
        self.lava = []
        self.pits = []
        self.doors = []
        self.items = []
        self.mobs = []
        self.kroz = []
        self.images = {}
        self.makeMap(game)
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
        self.moveable_walls = []
        self.lava = []
        self.pits = []
        self.doors = []
        self.items = []
        self.mobs = []
        self.kroz = []
    
    def moveWalls(self, game):
        available_spaces = []
        player_pos = game.player.rect
        for floor in game.level_map.floors:
            if (floor.top >= (player_pos.top + IMGSIZE) and floor.top <= (player_pos.top + IMGSIZE * 4)) or (floor.top <= (player_pos.top - IMGSIZE) and floor.top <= (player_pos.top - IMGSIZE * 4)):
                available_spaces.append(floor)
            if (floor.left >= (player_pos.left + IMGSIZE) and floor.left <= (player_pos.left + IMGSIZE * 4)) or (floor.left <= (player_pos.left - IMGSIZE) and floor.left <= (player_pos.left - IMGSIZE * 4)):
                available_spaces.append(floor)
            
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
            
                    
    def makeMap(self, game):
        if self.level % 2 == 1 or self.level == 20: #This checks to see if the level is odd, or the last level to load map otherwise random level 
            f = open(os.path.join(LVLDIR,'lvl{}.txt').format(self.level),'r')
            lines = f.readlines()
            self.level_map = lines
        
        else:    #this is where we read in the blank map, pass it to populate level then continue with the makemap
            f = open(os.path.join(LVLDIR, 'level.txt'),'r')
            lines = f.readlines()
            self.level_map = lines
            self.populateLevel(game)
            
        
        walls = ['#', '7', '8', 'X', 'Y', 'D', 'R', 'M','L','V','=', '/' ]
        
        for a in range(len(self.level_map)):
            for b in range(len(self.level_map[a])):
                y = a * IMGSIZE
                x = b * IMGSIZE
#---------------Walls, floors etc-----------------------------------------------------------------------------                

                if self.level_map[a][b] not in walls:
                    self.floors.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                    
                if self.level_map[a][b] == '#' or self.level_map[a][b] == '6' or self.level_map[a][b] == 'R':  
                    self.walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                
                if self.level_map[a][b] == 'X':
                    breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                    self.breakable.append(breakable_wall)
                if self.level_map[a][b] == 'Y':
                    breakable_wall =  RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                    self.triggered_walls['Y'].append(breakable_wall.rect)
                    self.breakable.append(breakable_wall)
               
                if self.level_map[a][b] == 'M':
                    moveable_wall = RLobject.MobTile(os.path.join(IMGDIR, 'breakable.bmp'), x, y)
                    self.breakable.append(moveable_wall)
                    self.moveable_walls.append(moveable_wall)
                        
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
                if self.level_map[a][b] == '/':
                    tree_wall = RLobject.Object(os.path.join(IMGDIR,'tree.bmp'), x, y)
                    self.breakable.append(tree_wall)
                
#----------------Player------------------------------------------------------------------------------------------                
                if self.level_map[a][b] == 'P':
                    game.player.rect.top = y
                    game.player.rect.left = x
                    
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
                    
                if self.level_map[a][b] == '?':
                    item = RLobject.Object(os.path.join(IMGDIR, 'sack.bmp'),x,y, 'gem_sack')
                    self.items.append(item)
                    
                if self.level_map[a][b] == 'B':
                    item = RLobject.Object(os.path.join(IMGDIR, 'bomb.bmp'),x,y, 'bomb')
                    self.items.append(item)
                    
                if self.level_map[a][b] == 'I':
                    item = RLobject.Object(os.path.join(IMGDIR, 'invisibility.bmp'),x,y, 'invisibility')
                    self.items.append(item)
                    
                if self.level_map[a][b] == 'Z':
                    item = RLobject.Object(os.path.join(IMGDIR, 'freeze_monster.bmp'),x,y, 'freeze')
                    self.items.append(item)
                    
                if self.level_map[a][b] == 'S':
                    item = RLobject.Object(os.path.join(IMGDIR, 'slow_monster.bmp'),x,y, 'slow')
                    self.items.append(item)
                   
                if self.level_map[a][b] == 'F':
                    item = RLobject.Object(os.path.join(IMGDIR, 'fast_monster.bmp'),x,y, 'fast')
                    self.items.append(item)
                   
                if self.level_map[a][b] == ']':
                    item = RLobject.Object(os.path.join(IMGDIR, 'sack.bmp'),x,y, 'more_monsters')
                    self.items.append(item)
                    
                if self.level_map[a][b] == '%':
                    item = RLobject.Object(os.path.join(IMGDIR, 'zap_monster.bmp'),x,y, 'zap')
                    self.items.append(item)
                    
                if self.level_map[a][b] == '!':
                    item = RLobject.Tablet(os.path.join(IMGDIR, 'tablet.bmp'),x,y, self.level)
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
                
                    
#---------------KROZ Letters------------------------------------------------------------------------------------------
                if self.level_map[a][b] == '<':
                    item = RLobject.Object(os.path.join(IMGDIR, 'k.bmp'),x,y, 'k')
                    self.items.append(item)
                    #self.triggers.append(item)
                if self.level_map[a][b] == '[':
                    item = RLobject.Object(os.path.join(IMGDIR, 'r.bmp'),x,y, 'r')
                    self.items.append(item)
                    #self.triggers.append(item)
                if self.level_map[a][b] == '|':
                    item = RLobject.Object(os.path.join(IMGDIR, 'o.bmp'),x,y, 'o')
                    self.items.append(item)
                    #self.triggers.append(item)
                if self.level_map[a][b] == '"':
                    item = RLobject.Object(os.path.join(IMGDIR, 'z.bmp'),x,y, 'z')
                    self.items.append(item)
                    #self.triggers.append(item)
        self.panel.messages.append('Press any key to start level')
        
    
    def populateLevel(self, game): # for randomly generated levels
        ''' grab self.level_map from MakeMap, find all the blank spaces, and fill them with junk based on level, and return map to Makemap
            need to randomly generate level content. different amounts based on level, mobs, breakable walls etc.
            must have:
            exit
            player start
        '''
        for a in range(len(self.level_map)):
            for b in range(len(self.level_map[a])):
                y = a * IMGSIZE
                x = b * IMGSIZE
                if self.level_map[a][b] == ' ':
                    self.floors.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                    
        
        #there are 1470 spaces available for random objects
        
        #add the exit
        space = random.randint(0, (len(self.floors) -1))
        self.exits.append(self.floors[space])
        self.floors.pop(space)
        
        #add Player Start
        space = random.randint(0, (len(self.floors) -1))
        game.player.rect = self.floors[space]
        self.floors.pop(space)
        
        
        if self.level == 2: #30% mobs 5% gems 5% whips 1 chest
            
            #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = RLobject.Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
            for e in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                trigger = Tile(x,y, False, 'teleport')
                self.triggers.append(trigger)
                self.items.append(item)
                self.floors.pop(space)
            for f in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
                
        if self.level == 4: #40% level 2 mobs some random items
             #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = RLobject.Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(588):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
            for e in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                trigger = Tile(x,y, False, 'teleport')
                self.triggers.append(trigger)
                self.items.append(item)
                self.floors.pop(space)
            for f in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
                    
        if self.level == 6: #80% breakable walls, whips gems, whip ring
             #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = RLobject.Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            
            #add a whip ring
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            ring = RLobject.Object(os.path.join(IMGDIR,'ring.bmp'), x , y, 'whip_ring')
            self.items.append(ring) 
            self.floors.pop(space)
             
               
           
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
            for f in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
        
        if self.level == 8:
            #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = RLobject.Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)    
            
        if self.level == 10:
            #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = RLobject.Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'ogre_lord.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
        
        if self.level == 12:
            #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = RLobject.Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)    
        
        if self.level == 14:
            for a in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = RLobject.Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                trigger = Tile(x,y, False, 'teleport')
                self.triggers.append(trigger)
                self.items.append(item)
                self.floors.pop(space)
            for b in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)
            for c in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR, 'invisibility.bmp'),x,y, 'invisibility')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(150):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'ogre_lord.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)                    
        if self.level == 16:
            for a in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                pit = RLobject.Object(os.path.join(IMGDIR,'pit.bmp'), x, y)
                self.pits.append(pit)
                self.floors.pop(space)
            for b in range(400):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)
            for c in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = RLobject.Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y)
                self.mobs.append(mob)
                self.floors.pop(space)
            for d in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
        
        if self.level == 18:
            for a in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = RLobject.Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)  
            for b in range(200):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'sack.bmp'), x, y, 'more_monsters')
                self.breakable.append(item)
                self.floors.pop(space)    
            for c in range (10):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = RLobject.Object(os.path.join(IMGDIR,'sack.bmp'), x, y, 'gem_sack')
                self.breakable.append(item)
                self.floors.pop(space)    
                
def renderAll(font, surface, testMap, images, player):
    surface.fill((0,0,0))

    testMap.panel.update(player, font, testMap)
    
    for a in range(len(testMap.level_map)):
        for b in range(len(testMap.level_map[a])):
            y = a * IMGSIZE # this sets the x and y coords by the number of pixels the image is, 16 ,32 etc.
            x = b * IMGSIZE
            surface.blit(images['floor'], (x,y))
                
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
        lava.draw(surface)
    for pit in testMap.pits:
        pit.draw(surface)
    if player.invisible == False: #only draw they player if they are not invisible
        player.draw(surface)
    if player.whipping == True:
        player.whip(surface, testMap)
        
        
    pygame.display.update() 