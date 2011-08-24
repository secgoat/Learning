#import pygame
import RLmap
from RLCONSTANTS import *
#from pygame.locals import *

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
        windowSurface.blit(images['floor'], (self.rect))
        pygame.display.update()
        
#--------------------------------------------------------------------------------
class Door(Object):
    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.locked = True
#--------------------------------------------------------------------------------
class Whip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('whip_anim.bmp').convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        #self.x = 0
        #self.y = 0
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)   
    
    def update(self, x, y,  degree = 0):
        self.image = pygame.transform.rotate(self.image, degree)
        self.rect.top = x
        self.rect.left = y
        
        
#------------------------------------------------------------------------------------    
class Mob(Object):
    
    def __init__(self, image, x,y):
        Object.__init__(self, image, x, y)
        self.kind = 'mob'
        self.view_range = 10 #set how sensitive the mob is to seeing the player and movign toward them
        
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
            if degree == 315:
                dx = -IMGSIZE
                dy = IMGSIZE
            
        newPosition = self.rect.move(dx, dy)
        oldPosition = self.rect
        
        if newPosition.collidelist(levelMap.walls) == -1: #check to see if colliding with walls -1 is False    
            if newPosition.collidelistall(levelMap.doors):
                self.rect = oldPosition
            else:    
                self.rect = newPosition
                
            if self.rect.colliderect(player.rect) == True:
                levelMap.mobs.remove(self)
                player.gems -= 1
        else:
            self.rect = oldPosition    
        
  
#-----------------------------------------------------------------------------------        
    
class Player(Object):
    
    def __init__(self, image, x, y):
        Object.__init__(self, image, x, y)
        self.whips = 5
        self.gems = 25
        self.maxGems = 150
        self.teleports = 0
        self.keys = 0
        self.score = 0
        self.weapon = Whip()
        self.whipping = False
    
    def teleport(self, levelMap):
        random_space = random.randint(1, len(levelMap.floors))
        
        print(random_space)
        self.rect = levelMap.floors(random_space).rect
        #dx = levelMap.floors[random_space].left
        #dy = levelMap.floors[random_space].top
        #self.move(dx,dy, levelMap)
        #self.move(dx, dy, levelMap)
    
    def move(self, dx, dy, levelMap):
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
                        #item.clear()
                        if item.kind == 'gem' and self.gems < self.maxGems:
                            self.gems += 1
                        if item.kind == 'whip':
                            self.whips += 1
                        if item.kind == 'gold':
                            self.score += 500
                        if item.kind == 'teleport':
                            self.teleports +=1
                        if item.kind == 'key':
                            self.keys +=1
                
            if newPosition.collidelistall(levelMap.doors):
                
                for item in levelMap.doors:
                    if item.rect == newPosition:
                        if self.keys > 0:
                            self.keys -= 1
                            levelMap.doors.remove(item)
                        else:
                            newPosition = oldPosition
            '''if newPosition.collidelist(levelMap.doors) == -1:
                pass
            else:
                for doors in levelMap.doors:
                    if doors.rect == newPosition and self.keys > 0:
                        self.keys -= 1
                        levelMap.doors.remove(doors)
                    else:
                        newPosition = oldPosition'''
        
            self.rect = newPosition
        else:
            self.rect = oldPosition
        
    def whip(self, surface):
        
        if self.whips > 0:
            x = self.rect.top -16
            y = self.rect.left
            self.weapon.update(x,y)
            self.weapon.draw(surface)
            '''endX,endY = rect.midtop
            pygame.draw.line(surface, (255,255,255), rect.midtop, (endX, endY - IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(20)'''
            
            x = self.rect.top
            y = self.rect.left - 16
            self.weapon.update(x,y, 45)
            self.weapon.draw(surface)
            '''
            pygame.draw.line(surface, (71,108,108), rect.midtop, (endX, endY - IMGSIZE), 2)
            #surface.blit(images['floor'], (endX, endY - IMGSIZE))
            endX,endY = rect.topleft
            pygame.draw.line(surface, (255,255,255), rect.topleft, (endX - IMGSIZE, endY - IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(20)
            
            #surface.blit(images['floor'], (endX - IMGSIZE, endY - IMGSIZE ))
            endX,endY = rect.midleft
            pygame.draw.line(surface, (255,255,255), rect.midleft, (endX - IMGSIZE, endY), 2)
            pygame.display.update()
            pygame.time.delay(20)
            
            #surface.blit(images['floor'], (endX - IMGSIZE, endY))
            endX,endY = rect.bottomleft
            pygame.draw.line(surface, (255,255,255), rect.bottomleft, (endX - IMGSIZE, endY + IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(20)
            
            #surface.blit(images['floor'], (endX - IMGSIZE, endY + IMGSIZE))
            endX,endY = rect.midbottom
            pygame.draw.line(surface, (255,255,255), rect.midbottom, (endX, endY + IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(20)
            
            #surface.blit(images['floor'], (endX, endY + IMGSIZE))
            endX,endY = rect.bottomright
            pygame.draw.line(surface, (255,255,255), rect.bottomright, (endX + IMGSIZE, endY + IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(20)
            
            #surface.blit(images['floor'], (endX + IMGSIZE, endY + IMGSIZE))
            endX,endY = rect.midright
            pygame.draw.line(surface, (255,255,255), rect.midright, (endX + IMGSIZE, endY), 2)
            pygame.display.update()
            pygame.time.delay(20)
            
            #surface.blit(images['floor'], (endX + IMGSIZE, endY))
            endX,endY = rect.topright
            pygame.draw.line(surface, (255,255,255), rect.topright, (endX + IMGSIZE, endY - IMGSIZE), 2)
            pygame.display.update()
            pygame.time.delay(20)
            
            #surface.blit(images['floor'], (endX + IMGSIZE, endY - IMGSIZE))'''
            self.whips -= 1
            self.whipping = False
        else:
            pass
            


    
