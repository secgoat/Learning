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
        self.rect = self.image.get_rect()
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)   
    
    def update(self, new_position,  frame = 1):
        #self.image = pygame.transform.rotate(self.image, degree)
        if frame == 1:
            self.image = pygame.image.load('whip_anim_1.bmp').convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
        if frame == 2:
            self.image = pygame.image.load('whip_anim_2.bmp').convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
        if frame == 3:
            self.image = pygame.image.load('whip_anim_3.bmp').convert()
            self.image.set_colorkey(self.image.get_at((0,0)))
        if frame == 4:
            self.image = pygame.image.load('whip_anim_4.bmp').convert()
            self.image.set_colorkey(self.image.get_at((1,0)))
        self.rect = new_position
        
    def checkCollision(self, level_map):
        if self.rect.collidelist(level_map.breakable) == -1:
            pass
        else:
            for item in level_map.breakable:
                if item == self.rect:
                    chance = random.randint(0,3)
                    if chance == 0:
                        level_map.breakable.remove(item)
        
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
            elif newPosition.collidelistall(levelMap.mobs):
                self.rect = oldPosition
            elif newPosition.collidelistall(levelMap.breakable):
                for wall in levelMap.breakable:
                    if wall.rect == newPosition:
                        levelMap.breakable.remove(wall)
                        levelMap.mobs.remove(self)
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
        self.whip_frame = 1
    
    def teleport(self, levelMap):
        random_space = random.randint(1, len(levelMap.floors))
        random_space = levelMap.floors.pop(random_space)
        print(random_space)
        self.rect = random_space
    
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
                        if item.kind == 'gem' and self.gems < self.maxGems:
                            self.gems += 1
                            levelMap.panel.messages.append('You pick up a gem. Points and Life!')
                        if item.kind == 'whip':
                            self.whips += 1
                        if item.kind == 'gold':
                            self.score += 500
                        if item.kind == 'teleport':
                            self.teleports +=1
                        if item.kind == 'key':
                            self.keys +=1
                        if item.kind == 'chest':
                            gem = random.randint(0,3)
                            whip = random.randint(0,3)
                            self.gems += gem
                            self.whips += whip
                            
                
            if newPosition.collidelistall(levelMap.doors):
                for item in levelMap.doors:
                    if item.rect == newPosition:
                        if self.keys > 0:
                            self.keys -= 1
                            levelMap.doors.remove(item)
                        else:
                            newPosition = oldPosition
                            
            if newPosition.collidelistall(levelMap.mobs):
                for mob in levelMap.mobs:
                    if mob.rect == newPosition:
                        self.gems -= 1
                        levelMap.mobs.remove(mob)
                        
            
            if newPosition.collidelistall(levelMap.breakable):
                for wall in levelMap.breakable:
                    if wall.rect == newPosition:
                        newPosition = oldPosition
                        
            if newPosition.collidelistall(levelMap.hidden_walls):
                for wall in levelMap.hidden_walls:
                    if wall == newPosition:
                        newPosition = oldPosition
                        levelMap.walls.append(wall)
                
            if newPosition.collidelistall(levelMap.exits):
                for level_exit in levelMap.exits:
                    if level_exit == newPosition:
                        levelMap.level += 1
                        levelMap.clearLevel()
                        levelMap.makeMap(self)
                        
                        #testMap = RLmap.Map(level, self)
                        
            self.rect = newPosition
        else:
            self.rect = oldPosition
        
    def whip(self, surface, testMap):
        if self.whip_frame >= 8:
            whip_frame = 1
        
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
            


    
