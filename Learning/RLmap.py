import os
from RLCONSTANTS import *
import RLpanel
from mob import Mob
from RLobject import Object, Door, Tablet
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
                    item = Object(os.path.join(IMGDIR, 'gem.bmp'), random_space.left, random_space.top, 'gem')
                    level_map.items.append(item)
            
            if self.kind == 'walls1':
                walls = level_map.triggered_walls['7']
                for wall in walls:
                    game.add_remove_walls.play()
                    level_map.walls.append(wall)
                level_map.panel.messages.append('The walls are closing in on you!')
            
            if self.kind == 'walls2':
                walls = level_map.triggered_walls['8']
                for wall in walls:
                    game.add_remove_walls.play()
                    level_map.walls.append(wall)
                level_map.panel.messages.append('The walls are closing in on you!')
            
            if self.kind == 'remove_walls':
                walls = level_map.triggered_walls['Y']
                for wall in walls:
                    game.add_remove_walls.play()
                    game.level_map.breakable.remove(wall)
                level_map.triggered_walls['Y'] = []
                
            if self.kind == 'move_walls':
                game.player.findMovingWalls(game)
                
            if self.kind == 'lava_flow':
                game.changeTimer(lava, VERYSLOW)
                
            if self.kind == "invis_walls":
                for a in range(100,200):
                    space = random.choice(game.level_map.walls)
                    game.level_map.walls.remove(space)
                    game.level_map.hidden_walls.append(space)
            if self.kind == 'earthquake':
                for a in range(50,100):
                    space = random.choice(game.level_map.floors)
                    breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), space.left,space.top)
                    game.level_map.breakable.append(breakable_wall)
            
            self.triggered = True
        else:
            return

class Map:
    def __init__(self, level, game):
        self.level = level
        self.map_of_level = []
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
                new_lava = Object(os.path.join(IMGDIR,'lava.bmp'), down.left, down.top)
                game.level_map.floors.remove(down)
                game.level_map.lava.append(new_lava)
                for item in game.level_map.items:
                    if item.rect == down:
                        game.level_map.items.remove(item)
                return
            if left in game.level_map.floors:
                new_lava = Object(os.path.join(IMGDIR,'lava.bmp'), left.left, left.top)
                game.level_map.floors.remove(left)
                game.level_map.lava.append(new_lava)
                for item in game.level_map.items:
                    if item.rect == left:
                        game.level_map.items.remove(item)
                return
            if right in game.level_map.floors:
                new_lava = Object(os.path.join(IMGDIR,'lava.bmp'), right.left, right.top)
                game.level_map.floors.remove(right)
                game.level_map.lava.append(new_lava)
                for item in game.level_map.items:
                    if item.rect == right:
                        game.level_map.items.remove(item)
                return
            if up in game.level_map.floors:
                new_lava = Object(os.path.join(IMGDIR,'lava.bmp'), up.left, up.top)
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
            self.map_of_level = lines
        
        else:    #this is where we read in the blank map, pass it to populate level then continue with the makemap
            f = open(os.path.join(LVLDIR, 'level.txt'),'r')
            lines = f.readlines()
            self.map_of_level = lines
            self.populateLevel(game)
            
        
        walls = ['#', '7', '8', 'X', 'Y', 'D', 'R', 'M','L','V','=', '/' ]
        
        for a in range(len(self.map_of_level)):
            for b in range(len(self.map_of_level[a])):
                y = a * IMGSIZE
                x = b * IMGSIZE
#---------------Walls, floors etc-----------------------------------------------------------------------------                

                if self.map_of_level[a][b] not in walls:
                    self.floors.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                    
                if self.map_of_level[a][b] == '#' or self.map_of_level[a][b] == '6' or self.map_of_level[a][b] == 'R':  
                    self.walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                
                if self.map_of_level[a][b] == 'X':
                    breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                    self.breakable.append(breakable_wall)
                if self.map_of_level[a][b] == 'Y':
                    breakable_wall =  Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                    self.triggered_walls['Y'].append(breakable_wall.rect)
                    self.breakable.append(breakable_wall)
               
                if self.map_of_level[a][b] == 'M':
                    moveable_wall = MobTile(os.path.join(IMGDIR, 'breakable.bmp'), x, y)
                    self.breakable.append(moveable_wall)
                    self.moveable_walls.append(moveable_wall)
                        
                if self.map_of_level[a][b] == 'D':
                    door = Door(os.path.join(IMGDIR,'door.bmp'), x, y)
                    self.doors.append(door)
                
                if self.map_of_level[a][b] == ':':
                    self.hidden_walls.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))
                
                if self.map_of_level[a][b] == '7':
                    wall = pygame.Rect(x,y,IMGSIZE,IMGSIZE)
                    self.triggered_walls['7'].append(wall) # uses a dictionary with a list as the value to keep track off all walls to be triggered
                
                if self.map_of_level[a][b] == '8':
                    wall = pygame.Rect(x,y,IMGSIZE,IMGSIZE)
                    self.triggered_walls['8'].append(wall)
                
                if self.map_of_level[a][b] == 'L':
                    self.exits.append(pygame.Rect(x,y,IMGSIZE,IMGSIZE))

                if self.map_of_level[a][b] == 'V':
                    lava = Object(os.path.join(IMGDIR,'lava.bmp'), x, y)
                    self.lava.append(lava)
                if self.map_of_level[a][b] == '=':
                    pit = Object(os.path.join(IMGDIR,'pit.bmp'), x, y)
                    self.pits.append(pit)
                if self.map_of_level[a][b] == 'R':
                    water = pygame.Rect(x,y,IMGSIZE,IMGSIZE)
                    self.water.append(water)
                if self.map_of_level[a][b] == '/':
                    tree_wall = Object(os.path.join(IMGDIR,'tree.bmp'), x, y)
                    self.breakable.append(tree_wall)
                
#----------------Player------------------------------------------------------------------------------------------                
                if self.map_of_level[a][b] == 'P':
                    game.player.rect.top = y
                    game.player.rect.left = x
                    
#-----------------MOBS-------------------------------------------------------------------------------                
                if self.map_of_level[a][b] == '1':
                    mob = Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y, 1, 'slow')
                    self.mobs.append(mob)
                
                if self.map_of_level[a][b] == '2':
                    mob = Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y, 2, 'medium')
                    self.mobs.append(mob)
                
                if self.map_of_level[a][b] == '3':
                    mob = Mob(os.path.join(IMGDIR,'ogre_lord.bmp'), x , y, 3, 'fast')
                    self.mobs.append(mob)
                
                if self.map_of_level[a][b] == '4':
                    mob = Mob(os.path.join(IMGDIR,'umber_hulk.bmp'), x , y, 3, 'fast')
                    self.mobs.append(mob)
#---------------Items-----------------------------------------------------------------                
                if self.map_of_level[a][b] == '+':
                    item = Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                    self.items.append(item)
                
                if self.map_of_level[a][b] == 'W':
                    item = Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                    self.items.append(item)
                
                if self.map_of_level[a][b] == 'T':
                    item = Object(os.path.join(IMGDIR,'teleport.bmp'), x , y, 'teleport')
                    self.items.append(item)
                
                if self.map_of_level[a][b] == 'K':
                    item = Object(os.path.join(IMGDIR,'key.bmp'), x , y, 'key')
                    self.items.append(item)
                
                if self.map_of_level[a][b] == '*':
                    item = Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                    self.items.append(item)
                
                if self.map_of_level[a][b] == 'C':
                    item = Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
                    self.items.append(item)

                if self.map_of_level[a][b] == 'Q':
                    item = Object(os.path.join(IMGDIR,'ring.bmp'),x,y,'whip_ring')
                    self.items.append(item)
                    
                if self.map_of_level[a][b] == '?':
                    item = Object(os.path.join(IMGDIR, 'sack.bmp'),x,y, 'gem_sack')
                    self.items.append(item)
                    
                if self.map_of_level[a][b] == 'B':
                    item = Object(os.path.join(IMGDIR, 'bomb.bmp'),x,y, 'bomb')
                    self.items.append(item)
                    
                if self.map_of_level[a][b] == '!':
                    item = Tablet(os.path.join(IMGDIR, 'tablet.bmp'),x,y, self.level)
                    self.items.append(item)
                    
#----------------SPELLS----------------------------------------------------------------------                    
                if self.map_of_level[a][b] == 'I':
                    item = Object(os.path.join(IMGDIR, 'invisibility.bmp'),x,y, 'invisibility')
                    self.items.append(item)
                    
                if self.map_of_level[a][b] == 'Z':
                    item = Object(os.path.join(IMGDIR, 'freeze_monster.bmp'),x,y, 'freeze')
                    self.items.append(item)
                    
                if self.map_of_level[a][b] == 'S':
                    item = Object(os.path.join(IMGDIR, 'slow_monster.bmp'),x,y, 'slow')
                    self.items.append(item)
                   
                if self.map_of_level[a][b] == 'F':
                    item = Object(os.path.join(IMGDIR, 'fast_monster.bmp'),x,y, 'fast')
                    self.items.append(item)
                   
                if self.map_of_level[a][b] == ']':
                    item = Object(os.path.join(IMGDIR, 'sack.bmp'),x,y, 'more_monsters')
                    self.items.append(item)
                    
                if self.map_of_level[a][b] == '%':
                    item = Object(os.path.join(IMGDIR, 'zap_monster.bmp'),x,y, 'zap')
                    self.items.append(item)
                    
                if self.map_of_level[a][b] == '.':
                    item = Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                    self.items.append(item)
                    
               
                    
#---------------Map Triggers-------------------------------------------------------------                    
                if self.map_of_level[a][b] == 'H':
                    trigger = Tile(x, y, False, 'gems')
                    self.triggers.append(trigger)
                
                if self.map_of_level[a][b] == '`':
                    trigger = Tile(x, y, False, 'walls1') #reveal hidden walls labeled as 7 on map
                    self.triggers.append(trigger)
                
                if self.map_of_level[a][b] == ',':
                    trigger = Tile(x, y, False, 'walls2') #reveal hidden walls labeled as 8 on map.
                    self.triggers.append(trigger)
                if self.map_of_level[a][b] == '~':
                    trigger = Tile(x, y, False, 'remove_walls')
                    self.triggers.append(trigger)
                
                if self.map_of_level[a][b] == 'A':
                    trigger = Tile(x,y, False, 'move_walls')
                    self.triggers.append(trigger)
                if self.map_of_level[a][b] == '9':
                    trigger = Tile(x,y, False, "lava_flow")
                    self.triggers.append(trigger)
                 
                if self.map_of_level[a][b] == 'N':
                    trigger = Tile(x,y,False,'invis_walls')
                    self.triggers.append(trigger)
                    
                if self.map_of_level[a][b] == 'E':
                    trigger = Tile(x,y,False,'earthquake')
                    self.triggers.append(trigger)
                
                    
#---------------KROZ Letters------------------------------------------------------------------------------------------
                if self.map_of_level[a][b] == '<':
                    item = Object(os.path.join(IMGDIR, 'k.bmp'),x,y, 'k')
                    self.items.append(item)
                    #self.triggers.append(item)
                if self.map_of_level[a][b] == '[':
                    item = Object(os.path.join(IMGDIR, 'r.bmp'),x,y, 'r')
                    self.items.append(item)
                    #self.triggers.append(item)
                if self.map_of_level[a][b] == '|':
                    item = Object(os.path.join(IMGDIR, 'o.bmp'),x,y, 'o')
                    self.items.append(item)
                    #self.triggers.append(item)
                if self.map_of_level[a][b] == '"':
                    item = Object(os.path.join(IMGDIR, 'z.bmp'),x,y, 'z')
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
        for a in range(len(self.map_of_level)):
            for b in range(len(self.map_of_level[a])):
                y = a * IMGSIZE
                x = b * IMGSIZE
                if self.map_of_level[a][b] == ' ':
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
            chest = Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y,1,'slow')
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
            for e in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                trigger = Tile(x,y, False, 'teleport')
                self.triggers.append(trigger)
                self.items.append(item)
                self.floors.pop(space)
            for f in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
                
        if self.level == 4: #40% level 2 mobs some random items
             #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(588):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y,2,'medium')
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
            for e in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                trigger = Tile(x,y, False, 'teleport')
                self.triggers.append(trigger)
                self.items.append(item)
                self.floors.pop(space)
            for f in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
                    
        if self.level == 6: #80% breakable walls, whips gems, whip ring
             #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            
            #add a whip ring
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            ring = Object(os.path.join(IMGDIR,'ring.bmp'), x , y, 'whip_ring')
            self.items.append(ring) 
            self.floors.pop(space)
             
               
           
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(14):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
            for f in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
        
        if self.level == 8:
            #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y,1,'slow')
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)    
            
        if self.level == 10:
            #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y,1,'slow')
                self.mobs.append(mob)
                self.floors.pop(space)
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y,2,'medium')
                self.mobs.append(mob)
                self.floors.pop(space)
            for a in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'ogre_lord.bmp'), x , y,3,'fast')
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)    
        
        if self.level == 12:
            #add a chest
            space = random.randint(0, (len(self.floors) -1))
            x = self.floors[space].left
            y = self.floors[space].top
            chest = Object(os.path.join(IMGDIR,'chest.bmp'), x , y, 'chest')
            self.items.append(chest) 
            self.floors.pop(space)
            #add a slow monsters
             
            #add a teleport
             
               
            for a in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'elf_mummy.bmp'), x , y,2,'medium')
                self.mobs.append(mob)
                self.floors.pop(space)
            for b in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gem.bmp'), x, y, 'gem')
                self.items.append(item)
                self.floors.pop(space)
            for c in range(73):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR,'whip.bmp'), x , y, 'whip')
                self.items.append(item)
                self.floors.pop(space)    
        
        if self.level == 14:
            for a in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                item = Object(os.path.join(IMGDIR, 'tele_trap.bmp'), x, y, 'tele_trap')
                trigger = Tile(x,y, False, 'teleport')
                self.triggers.append(trigger)
                self.items.append(item)
                self.floors.pop(space)
            for b in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)
            for c in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR, 'invisibility.bmp'),x,y, 'invisibility')
                self.items.append(item)
                self.floors.pop(space)
            for d in range(150):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'ogre_lord.bmp'), x , y,3,'fast')
                self.mobs.append(mob)
                self.floors.pop(space)                    
        if self.level == 16:
            for a in range(300):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top    
                pit = Object(os.path.join(IMGDIR,'pit.bmp'), x, y)
                self.pits.append(pit)
                self.floors.pop(space)
            for b in range(400):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)
            for c in range(241):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                mob = Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y,1,'slow')
                self.mobs.append(mob)
                self.floors.pop(space)
            for d in range(140):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'gold.bmp'), x , y, 'gold')
                self.items.append(item)
                self.floors.pop(space)  
        
        if self.level == 18:
            for a in range(1000):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                breakable_wall = Object(os.path.join(IMGDIR,'breakable.bmp'), x, y)
                self.breakable.append(breakable_wall)
                self.floors.pop(space)  
            for b in range(200):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'sack.bmp'), x, y, 'more_monsters')
                self.items.append(item)
                self.floors.pop(space)    
            for c in range (10):
                space = random.randint(0, (len(self.floors) -1))
                x = self.floors[space].left
                y = self.floors[space].top
                item = Object(os.path.join(IMGDIR,'sack.bmp'), x, y, 'gem_sack')
                self.items.append(item)
                self.floors.pop(space)    
                
def renderAll(game):
    game.surface.fill((0,0,0))

    game.level_map.panel.update(game.player, game.font, game.level_map)
    
    for a in range(len(game.level_map.map_of_level)):
        for b in range(len(game.level_map.map_of_level[a])):
            y = a * IMGSIZE # this sets the x and y coords by the number of pixels the image is, 16 ,32 etc.
            x = b * IMGSIZE
            game.surface.blit(images['floor'], (x,y))
                
    #draw all objects in the lists
    for wall in game.level_map.walls:
        game.surface.blit(images['wall'], wall)
    for water in game.level_map.water:
        game.surface.blit(images['water'], water)
    for stairs in game.level_map.exits:
        game.surface.blit(images['stairs'], stairs)
    for item in game.level_map.items:
        item.draw(game.surface)
    for mob in game.level_map.mobs:
        mob.draw(game.surface)
    for door in game.level_map.doors:
        door.draw(game.surface)
    for breakable_wall in game.level_map.breakable:
        breakable_wall.draw(game.surface)
    for lava in game.level_map.lava:
        lava.draw(game.surface)
    for pit in game.level_map.pits:
        pit.draw(game.surface)
    if game.player.invisible == False: #only draw they player if they are not invisible
        game.player.draw(game.surface)
    if game.player.whipping == True:
        game.player.whip(game)
        
        
    pygame.display.update() 