import pygame
import RLmap, anim
import math, random
from RLCONSTANTS import *
from pygame.locals import *

class Object(pygame.sprite.Sprite):
    #this is a generic object: player, monster, chest , stairs etc.
    def __init__(self, image, x, y, kind = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        #self.image.set_colorkey((71,108,108))
        self.image.set_colorkey(self.image.get_at((0,0))) # makes the border color transparent no matter what!
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.kind = kind
         
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def clear(self):
        windowSurface.blit(images['floor'], self.rect)
        pygame.display.update()
        
#--------------------------------------------------------------------------------
class Door(Object):
    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.locked = True
#--------------------------------------------------------------------------------
class Tablet(Object):
    def __init__(self, image, x, y, level):
        Object.__init__(self, image, x, y)
        self.message = ' '
        self.kind = 'tablet'
        self.level = level
        self.setMessage()
        
    def setMessage(self):
        if self.level == 1:
            self.message = 'Remember to experiment with every new object on a level.'
        if self.level == 3:
            self.message = 'Only use your valuable Teleports for last chance escapes!'
        if self.level == 5:
            self.message = 'You\'re right in the middle of a Lava Flow!  Run for it!'
        if self.level == 7:
            self.message = 'You\'ll need the two keys from the previous level!'
        if self.level == 9:
            self.message = 'The two chests can be yours if you find the hidden spell!'
        if self.level == 11:
            self.message = 'You learn from successful failures.'
        if self.level == 13:
            self.message = 'A Creature Generator exists within this chamber--destroy it!'
        if self.level == 15:
            self.message = 'By throwing dirt at someone you only lose ground.'
        if self.level == 17:
            self.message = 'The Bubble Creatures knock off three Gems when touched!'
        if self.level == 19:
            self.message = 'Be vigilant Adventurer, the Crown is near, but well protected.'
        if self.level == 20:
            self.message = 'You\'ve survived so far, Adventurer.  Can you succeed?'
#----------------------------------------------------------------------------- -
class Whip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(IMGDIR,'whip_anim.bmp')).convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()
        self.power = 1
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)   
    
    def update(self, new_position,  frame = 1):
        if frame == 1:
            self.image = pygame.image.load(os.path.join(IMGDIR,'whip_anim_1.bmp')).convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
        if frame == 2:
            self.image = pygame.image.load(os.path.join(IMGDIR,'whip_anim_2.bmp')).convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
        if frame == 3:
            self.image = pygame.image.load(os.path.join(IMGDIR,'whip_anim_3.bmp')).convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
        if frame == 4:
            self.image = pygame.image.load(os.path.join(IMGDIR,'whip_anim_4.bmp')).convert()
            self.image.set_colorkey(self.image.get_at((1,0)))
        self.rect = new_position
        
    def checkCollision(self, level_map):
        if self.rect.collidelist(level_map.breakable) == -1:
            pass
        else:
            for item in level_map.breakable:
                if item == self.rect:
                    chance = random.randint(0,(4 - self.power))
                    if chance == 0:
                        level_map.breakable.remove(item)
                        level_map.floors.append(item)
                        #TODO: remove triggered walls Y 7 8 from triggered wall list as well
                        if item.rect in level_map.triggered_walls['Y']:
                            level_map.triggered_walls['Y'].remove(item.rect)
        if self.rect.collidelist(level_map.mobs) == -1:
            pass
        else:
            for mob in level_map.mobs:
                if mob.rect == self.rect:
                    level_map.mobs.remove(mob)
                
        
        
#------------------------------------------------------------------------------------    
class Mob(Object):
    
    def __init__(self, image, x,y):
        Object.__init__(self, image, x, y)
        self.kind = 'mob'
        self.view_range = 5 #set how sensitive the mob is to seeing the player and movign toward them
        
    def checkDistance(self, player):
        distance = abs(math.sqrt(math.pow((player.rect.centerx - self.rect.centerx),2) + math.pow((player.rect.centery - self.rect.centery),2))) / IMGSIZE
        # this gets the distance between 2 points. absolute value so it is a positive number, pow raises first part by second part Ie X to the power of 2. and then divide by IMGsize to fidn how many squares on the map away the player is from the mob.
        return distance
    
    def move(self, player, levelMap):
        dy = 0
        dx = 0
        if self.checkDistance(player) <= self.view_range:
            radian = math.atan2(self.rect.centery - player.rect.centery, self.rect.centerx - player.rect.centerx) 
            # radian shows the angle between mob and player. then need to turn it into degrees and make it a positive degree so my brain can comprehend easier.
            degree = math.degrees(radian)        
            if degree < 0:
                degree = degree + 360
            degree = int(degree) #degrees from mob to player
            #print(radian, degree)
            if degree == 0 or (degree > 0 and degree < 23) or (degree > 293 and degree < 359) :
                dx = -IMGSIZE
                dy = 0
            if degree == 45 or (degree < 45 and degree < 23) or (degree > 45 and degree < 68):
                dx = -IMGSIZE
                dy = -IMGSIZE
            if degree == 90 or (degree < 90 and degree > 68) or (degree > 90 and degree < 113):
                dx = 0
                dy = -IMGSIZE
            if degree == 135 or (degree < 135 and degree > 113) or (degree > 135 and degree < 157):
                dx = IMGSIZE
                dy = -IMGSIZE
            if degree == 180 or (degree < 180 and degree > 157) or (degree > 180 and degree < 203):
                dx = IMGSIZE
                dy = 0
            if degree == 225 or (degree < 225 and degree > 203) or (degree > 225 and degree < 248):
                dx = IMGSIZE
                dy = IMGSIZE
            if degree == 270 or (degree < 270 and degree > 248) or (degree > 270 and degree < 293):
                dx = 0
                dy = IMGSIZE
            if degree == 315 or (degree < 315 and degree > 293):
                dx = -IMGSIZE
                dy = IMGSIZE
            
        newPosition = self.rect.move(dx, dy)
        oldPosition = self.rect
        
        if newPosition.collidelist(levelMap.walls) == -1: #check to see if colliding with walls -1 is False    
            if newPosition.collidelistall(levelMap.doors):
                self.rect = oldPosition
            elif newPosition.collidelistall(levelMap.mobs):
                self.rect = oldPosition
            elif newPosition.collidelistall(levelMap.breakable):
                for wall in levelMap.breakable:
                    if wall.rect == newPosition  and (self.kind != 'mob tile'):
                        levelMap.breakable.remove(wall)
                        levelMap.mobs.remove(self)
            else:    
                self.rect = newPosition
                
            if self.rect.colliderect(player.rect) == True:
                if self.kind != 'mob tile':
                    levelMap.mobs.remove(self)
                    player.gems -= 1
                else:
                    self.rect = oldPosition
                    return
            if self.rect.collidelistall(levelMap.items) and (self.kind != 'mob tile'):
                for item in levelMap.items:
                    if item.rect == newPosition:
                        levelMap.items.remove(item)
        else:
            self.rect = oldPosition    
        
#--------------------------------------------------------------------------------------

class MobTile(Mob):
    def __init__(self, image,x,y):
        Mob.__init__(self, image, x, y)
        self.moving = False
        self.kind = 'mob tile'  
#-----------------------------------------------------------------------------------        
    
class Player(Object):
    
    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.whips = 5
        self.gems = 20
        self.maxGems = 150
        self.teleports = 0
        self.keys = 0
        self.score = 0
        self.invisible = False
        self.weapon = Whip()
        self.whipping = False
        self.whip_frame = 1
    
    def findMovingWalls(self, game):
        '''
        need to grab a circle around the player, use 3 blocks (IMGSIZE *3) = pi radius squared
         grab list of blocks that fall in that circumference.
         check list against position of moving walls
         
         means i need to create a moving wall object with an Activated attribute. If activated
         it will travel just like a mob toward the player.
        '''
        center_x = self.rect.centerx
        center_y = self.rect.centery
        radius = IMGSIZE * 4
        
        for wall in game.level_map.moveable_walls:
            x = wall.rect.centerx
            y = wall.rect.centery
            if game.isInRange(center_x, center_y, radius, x,y):
                wall.moving = True
                

    def teleport(self, game):
        levelMap = game.level_map
        random_space = random.randint(1, len(levelMap.floors))
        random_space = levelMap.floors.pop(random_space)
        #print(random_space)
        self.rect = random_space
    
    def move(self, dx, dy, game):
        levelMap = game.level_map
        
        ''' add collision detection if player hits mob, 
        currently works if mob hits player but not the other way around'''
        newPosition = self.rect.move(dx, dy)
        oldPosition = self.rect
        if newPosition.collidelist(levelMap.walls) == -1: #check to see if colliding with walls -1 is False
            if newPosition.collidelist(levelMap.items) == -1: #check to see if colliding with items
                pass
            else:
                for item in levelMap.items: #iterate through items and remove them from the map and the list
                    if item.rect == newPosition:
                        levelMap.items.remove(item)
                        if item.kind == 'gem' and self.gems < self.maxGems:
                            self.gems += 1
                            levelMap.panel.messages.append('You pick up a gem. Points and Life!')
                        if item.kind == 'whip':
                            self.whips += 1
                            levelMap.panel.messages.append('You pick up a Whip.')
                        if item.kind == 'gold':
                            self.score += 500
                            levelMap.panel.messages.append('You pick up a pile of gold.')
                        if item.kind == 'teleport':
                            self.teleports +=1
                            levelMap.panel.messages.append('A teleport scroll.')
                        if item.kind == 'key':
                            self.keys +=1
                            levelMap.panel.messages.append('A key.')
                        if item.kind == 'chest':
                            gem = random.randint(0,3)
                            whip = random.randint(0,3)
                            levelMap.panel.messages.append('You open a treasure chest and find {0} gems and {1} whips.'.format(gem,whip))
                            self.gems += gem
                            self.whips += whip
                        if item.kind == 'whip_ring':
                            self.weapon.power += 1
                            levelMap.panel.messages.append('You find a ring of Whip Power!')
                        if item.kind == 'gem_sack':
                            self.gems += 25
                            levelMap.panel.messages.append('You found a pouch with 25 Gems')
                        if item.kind == 'bomb':
                            center_x = item.rect.centerx
                            center_y = item.rect.centery
                            radius = IMGSIZE * 5
                            for wall in game.level_map.breakable:
                                x = wall.rect.centerx
                                y = wall.rect.centery
                                if game.isInRange(center_x, center_y, radius, x,y):
                                    game.level_map.breakable.remove(wall)
                                    game.level_map.moveable_walls.remove(wall)
                        if item.kind == 'k' or item.kind =='r' or item.kind == 'o' or item.kind == 'z':
                            game.level_map.kroz.append(item.kind)
                            if len(game.level_map.kroz) == 4: 
                                if game.level_map.kroz[0] == 'k' and game.level_map.kroz[1] == 'r' and game.level_map.kroz[2] == 'o' and game.level_map.kroz[3] == 'z':
                                    game.player.score += 10000
                                    #play a sound
                                    game.level_map.panel.messages.append('You get the KROZ 10,000 point bonus!')
                        if item.kind == 'freeze':
                            game.stopTimers()
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger a freeze monster spell!')
                        if item.kind == 'slow':
                            game.slowTimers()
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger a slow monster spell!')
                        if item.kind == 'fast':
                            game.speedTimers()
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger a speed monster spell!')
                        if item.kind == 'invisibility':
                            game.player.invisible = True
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger an invisibiltiy spell!')
                        if item.kind == 'tablet':
                            game.player.score += 10000
                            game.level_map.panel.messages.append(item.message)
                            
                            
#--------------------------------------------------------------------------------------------------------------------------------------
            if newPosition.collidelistall(levelMap.triggers): #triggers that set of special events etc
                for trigger in levelMap.triggers:
                    if trigger.rect == newPosition:
                        trigger.trigger(game)
                        if trigger.kind == 'teleport':
                            game.level_map.triggers.remove(trigger)
                            return
                            #newPosition = self.rect
                       
                
                
            if newPosition.collidelistall(levelMap.doors): #locked doors
                for item in levelMap.doors:
                    if item.rect == newPosition:
                        if self.keys > 0:
                            self.keys -= 1
                            levelMap.doors.remove(item)
                        else:
                            newPosition = oldPosition
                            
            if newPosition.collidelistall(levelMap.mobs): #collision with mobs
                for mob in levelMap.mobs:
                    if mob.rect == newPosition:
                        self.gems -= 1
                        levelMap.mobs.remove(mob)
                        
            
            if newPosition.collidelistall(levelMap.breakable): #breakable is a list of breakable walls, needed to seperate from regular walls
                for wall in levelMap.breakable:
                    if wall.rect == newPosition:
                        newPosition = oldPosition
                        
            if newPosition.collidelistall(levelMap.hidden_walls): # this is the hidden walls, maybe only level 1? when bumped it appears
                for wall in levelMap.hidden_walls: 
                    if wall == newPosition:
                        newPosition = oldPosition
                        levelMap.walls.append(wall)
                
                
            if newPosition.collidelistall(levelMap.exits): #did they get to the level exit?
                for level_exit in levelMap.exits:
                    if level_exit == newPosition:
                        levelMap.level += 1
                        game.level_map.clearLevel()
                        RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
                        game.clock.tick(2)
                        game.level_map.makeMap(game)
                        RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
                        while not pygame.event.wait().type in (QUIT, KEYDOWN):
                            pass
                        return
            if newPosition.collidelistall(levelMap.pits):
                anim.pitFall(game)
                
            if newPosition.collidelistall(levelMap.lava): #lava collision
                for lava in levelMap.lava:
                    if lava.rect == newPosition:
                        self.gems -= 10
                        levelMap.lava.remove(lava)
                        levelMap.floors.append(lava.rect)
                        
            self.rect = newPosition
        else:
            self.rect = oldPosition
        
    def whip(self, surface, testMap):
        #if self.whip_frame >= 8:
            #whip_frame = 1
        
        if self.whips > 0:
            
            if self.whip_frame == 1:
                new_position = self.rect.move(0, -IMGSIZE)
                self.weapon.update(new_position, 1)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 2:
                new_position = self.rect.move(-IMGSIZE, -IMGSIZE)
                self.weapon.update(new_position, 2)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame += 1
                return
         
            if self.whip_frame == 3:
                new_position = self.rect.move(-IMGSIZE, 0)
                self.weapon.update(new_position, 3)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 4:
                new_position = self.rect.move(-IMGSIZE, IMGSIZE)
                self.weapon.update(new_position, 4)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 5:
                new_position = self.rect.move(0, IMGSIZE)
                self.weapon.update(new_position, 1)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 6:
                new_position = self.rect.move(IMGSIZE, IMGSIZE)
                self.weapon.update(new_position, 2)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 7:
                new_position = self.rect.move(IMGSIZE, 0)
                self.weapon.update(new_position, 3)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame += 1
                return
                
            if self.whip_frame == 8:
                new_position = self.rect.move(IMGSIZE, -IMGSIZE)
                self.weapon.update(new_position, 4)
                self.weapon.draw(surface)
                self.weapon.checkCollision(testMap)
                self.whip_frame = 1
                self.whips -= 1
                self.whipping = False
                return
           
        else:
            pass
            


    
