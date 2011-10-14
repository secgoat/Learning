import pygame
import math, random
from RLCONSTANTS import *
from RLobject import Object
from pygame.locals import *

class Mob(Object):
    
    def __init__(self, image, x,y, damage, speed):
        Object.__init__(self, image, x, y)
        self.kind = 'mob'
        self.view_range = 5 #set how sensitive the mob is to seeing the player and movign toward them
        self.damage = damage
        self.speed = speed
        
    def checkDistance(self, player):
        distance = abs(math.sqrt(math.pow((player.rect.centerx - self.rect.centerx),2) + math.pow((player.rect.centery - self.rect.centery),2))) / IMGSIZE
        # this gets the distance between 2 points. absolute value so it is a positive number, pow raises first part by second part Ie X to the power of 2. and then divide by IMGsize to find how many squares on the map away the player is from the mob.
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
            
        new_position = self.rect.move(dx, dy)
        old_position = self.rect
        self.rect = self.checkCollision(game,new_position,old_position)
        
    def checkCollision(self, game, new_position, old_position):
        position = old_position
        if new_position.collidelist(game.level_map.walls) == -1: #check to see if colliding with walls -1 is False    
            if new_position.collidelistall(game.level_map.doors):
                position = old_position
            elif new_position.collidelistall(game.level_map.mobs):
                position = old_position
            elif new_position.collidelistall(game.level_map.breakable):
                for wall in game.level_map.breakable:
                    if wall.rect == new_position  and (self.kind != 'mob tile'):
                        game.level_map.breakable.remove(wall)
                        game.level_map.mobs.remove(self)
            else:    
                position = new_position
                
            if position.colliderect(game.player.rect) == True:
                if self.kind != 'mob tile':
                    game.level_map.mobs.remove(self)
                    game.player.gems -= self.damage
                    game.mob_hit_player.play()
                    
                else:
                    position = old_position
                    #return position
            if self.rect.collidelistall(game.level_map.items) and (self.kind != 'mob tile'):
                for item in game.level_map.items:
                    if item.rect == new_position:
                        game.level_map.items.remove(item)
        else:
            position = old_position
        
        return position    
        
#--------------------------------------------------------------------------------------

class MobTile(Mob):
    def __init__(self, image,x,y):
        Mob.__init__(self, image, x, y,1,'slow')
        self.moving = False
        self.kind = 'mob tile'  
#-----------------------------------------------------------------------------------        
    
