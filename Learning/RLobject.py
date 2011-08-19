#import pygame
import RLmap
from RLCONSTANTS import *
#from pygame.locals import *

class Object(pygame.sprite.Sprite):
    #this is a generic object: player, monster, chest , stairs etc.
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey((71,108,108))
        self.rect = self.image.get_rect()
        self.rect.top = x
        self.rect.left = y
        self.kind = None
         
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def clear(self):
        windowSurface.blit(images['floor'], (self.rect))
        pygame.display.update()
        
    
class Mob(Object):
    
    def __init__(self, image, x,y):
        Object.__init__(self, image, x, y)
        self.kind = 'mob'
        
    
    
class Player(Object):
    
    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.whips = 5
        self.gems = 100
        self.maxGems = 100
        self.teleports = 0
        self.keys = 0
        self.score = 0
        self.whipping = False
    
    def move(self, dx, dy, levelMap):
        newPosition = self.rect.move(dx, dy)
        oldPosition = self.rect
        if newPosition.collidelist(levelMap.walls) == -1: #check to see if colliding with walls -1 is False
            if newPosition.collidelist(levelMap.items) == -1: #check to see if colliding with items
                pass
            else:
                for item in levelMap.items: #iterate through items and remove them from the map and the list
                    if item.rect == newPosition:
                        levelMap.items.remove(item)
                        item.clear()
                        if item.kind == 'gem' and self.gems < self.maxGems:
                            self.gems += 1
                        if item.kind == 'whip':
                            self.whips += 1
                    
                    
            self.rect = newPosition
        else:
            self.rect = oldPosition
        
    def whip(self, surface, rect):
        if self.whips > 0:
            endX,endY = rect.midtop
            pygame.draw.line(surface, (255,255,255), rect.midtop, (endX, endY - IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(30)
            endX,endY = rect.midtop
            
            endX,endY = rect.topleft
            pygame.draw.line(surface, (255,255,255), rect.topleft, (endX - IMGSIZE, endY - IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(30)
            
            endX,endY = rect.midleft
            pygame.draw.line(surface, (255,255,255), rect.midleft, (endX - IMGSIZE, endY), 2)
            pygame.display.update()
            pygame.time.delay(30)
            
            endX,endY = rect.bottomleft
            pygame.draw.line(surface, (255,255,255), rect.bottomleft, (endX - IMGSIZE, endY + IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(30)
            
            endX,endY = rect.midbottom
            pygame.draw.line(surface, (255,255,255), rect.midbottom, (endX, endY + IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(30)
            
            endX,endY = rect.bottomright
            pygame.draw.line(surface, (255,255,255), rect.bottomright, (endX + IMGSIZE, endY + IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(30)
            
            endX,endY = rect.midright
            pygame.draw.line(surface, (255,255,255), rect.midright, (endX + IMGSIZE, endY), 2)
            pygame.display.update()
            pygame.time.delay(30)
            
            endX,endY = rect.topright
            pygame.draw.line(surface, (255,255,255), rect.topright, (endX + IMGSIZE, endY - IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(30)
            
            self.whips -= 1
            self.whipping = False
        else:
            pass
            

    

    
