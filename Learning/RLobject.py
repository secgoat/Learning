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
                
        