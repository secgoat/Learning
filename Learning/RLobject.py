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
        self.image.set_colorkey(self.image.get_at((0,0))) # makes the border color transparent no matter what!
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.kind = kind
         
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        
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
        
    def checkCollision(self, game):
        if self.rect.collidelist(game.level_map.breakable) == -1:
            pass
        else:
            for item in game.level_map.breakable:
                if item == self.rect:
                    game.whip_breakable.play()
                    chance = random.randint(0,(4 - self.power))
                    if chance == 0:
                        game.level_map.breakable.remove(item)
                        game.level_map.floors.append(item)
                        #TODO: remove triggered walls Y 7 8 from triggered wall list as well
                        if item.rect in game.level_map.triggered_walls['Y']:
                            game.level_map.triggered_walls['Y'].remove(item.rect)
        if self.rect.collidelist(game.level_map.mobs) == -1:
            pass
        else:
            for mob in game.level_map.mobs:
                if mob.rect == self.rect:
                    game.level_map.mobs.remove(mob)
                
        
        
#------------------------------------------------------------------------------------    
class Mob(Object):
    
    def __init__(self, image, x,y, damage, speed):
        Object.__init__(self, image, x, y)
        self.kind = 'mob'
        self.view_range = 5 #set how sensitive the mob is to seeing the player and movign toward them
        self.damage = damage
        self.speed = speed
        
    def checkDistance(self, player):
        distance = abs(math.sqrt(math.pow((player.rect.centerx - self.rect.centerx),2) + math.pow((player.rect.centery - self.rect.centery),2))) / IMGSIZE
        # this gets the distance between 2 points. absolute value so it is a positive number, pow raises first part by second part Ie X to the power of 2. and then divide by IMGsize to fidn how many squares on the map away the player is from the mob.
        return distance
    
    def move(self, game):
        player = game.player
        levelMap = game.level_map
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
                    player.gems -= self.damage
                    game.mob_hit_player.play()
                    
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
        Mob.__init__(self, image, x, y,1,'slow')
        self.moving = False
        self.kind = 'mob tile'  
#-----------------------------------------------------------------------------------        
    

            


    
