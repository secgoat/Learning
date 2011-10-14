import pygame
import RLmap, anim
import math, random
from RLCONSTANTS import *
from RLobject import Object, Whip
from mob import Mob, MobTile
from pygame.locals import *


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
        radius = IMGSIZE * 10
        
        for wall in game.level_map.moveable_walls:
            x = wall.rect.centerx
            y = wall.rect.centery
            if game.isInRange(center_x, center_y, radius, x,y):
                wall.moving = True
                

    def teleport(self, game):
        random_space = random.choice(game.level_map.floors)
        new_position = random_space
        old_position = self.rect
        temp_space = self.checkCollision(game, old_position, new_position)
        check_again = False
        if temp_space == old_position:
            check_again = True
        while check_again == True:
            random_space = random.choice(game.level_map.floors)
            temp_space = self.checkCollision(game, old_position, random_space)
            if temp_space != old_position:
                check_again = False
        return temp_space
            
            
    
    def move(self, dx, dy, game):
        ''' add collision detection if player hits mob, 
        currently works if mob hits player but not the other way around'''
        new_position = self.rect.move(dx, dy)
        old_position = self.rect
        self.rect = self.checkCollision(game, old_position, new_position )
    
    def checkCollision(self, game, old_position, new_position):
        position = old_position
        if new_position.collidelist(game.level_map.walls) == -1: #check to see if colliding with walls -1 is False
            if new_position.collidelist(game.level_map.items) == -1: #check to see if colliding with items
                pass
            else:
                for item in game.level_map.items: #iterate through items and remove them from the map and the list
                    if item.rect == new_position:
                        game.level_map.items.remove(item)
                        if item.kind == 'gem' and self.gems < self.maxGems:
                            self.gems += 1
                            self.score += 10
                            game.level_map.panel.messages.append('You pick up a gem. Points and Life!')
                        if item.kind == 'whip':
                            self.whips += 1
                            self.score =+ 10
                            game.level_map.panel.messages.append('You pick up a Whip.')
                        if item.kind == 'gold':
                            game.gold.play()
                            self.score += 500
                            game.level_map.panel.messages.append('You pick up a pile of gold.')
                        if item.kind == 'teleport':
                            self.teleports +=1
                            self.score += 10
                            game.level_map.panel.messages.append('A teleport scroll.')
                        if item.kind == 'key':
                            self.keys +=1
                            self.score += 10
                            game.level_map.panel.messages.append('A key.')
                        if item.kind == 'chest':
                            gem = random.randint(0,3)
                            whip = random.randint(0,3)
                            game.level_map.panel.messages.append('You open a treasure chest and find {0} gems and {1} whips.'.format(gem,whip))
                            self.gems += gem
                            self.whips += whip
                            self.score += 50 
                        if item.kind == 'whip_ring':
                            self.weapon.power += 1
                            self.score += 1000
                            game.level_map.panel.messages.append('You find a ring of Whip Power!')
                        if item.kind == 'gem_sack':
                            self.gems += 25
                            self.score += 125
                            game.level_map.panel.messages.append('You found a pouch with 25 Gems')
                        if item.kind == 'bomb':
                            game.bomb.play()
                            self.score += 500
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
                        if item.kind == 'tele_trap':
                            position = self.teleport(game)
                            return position
#---SPELLS-----------------------------------------                        
                        if item.kind == 'freeze':
                            game.stopTimers()
                            self.score += 10
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger a freeze monster spell!')
                        if item.kind == 'slow':
                            game.slowTimers()
                            self.score += 10
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger a slow monster spell!')
                        if item.kind == 'fast':
                            game.speedTimers()
                            self.score += 10
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger a speed monster spell!')
                        if item.kind == 'invisibility':
                            game.player.invisible = True
                            self.score += 100
                            game.changeTimer(check_things,ETERNITY)
                            game.level_map.panel.messages.append('You trigger an invisibiltiy spell!')
                        if item.kind == 'more_monsters':
                            for a in range(20,50):
                                space = random.choice(game.level_map.floors)
                                x = space.left
                                y = space.top
                                mob = Mob(os.path.join(IMGDIR,'gnome.bmp'), x , y, 1, 'slow')
                                game.level_map.mobs.append(mob)
                        
                        if item.kind == 'tablet':
                            game.player.score += 10000
                            game.level_map.panel.messages.append(item.message)                  
#TRIGGERS-----------------------------------------------------------------------------------------------------------------------------------
            if new_position.collidelistall(game.level_map.triggers): #triggers that set of special events etc
                for trigger in game.level_map.triggers:
                    if trigger.rect == new_position:
                        trigger.trigger(game)
                       
                
            if new_position.collidelistall(game.level_map.doors): #locked doors
                for item in game.level_map.doors:
                    if item.rect == new_position:
                        if self.keys > 0:
                            self.keys -= 1
                            game.level_map.doors.remove(item)
                        else:
                            game.hit_wall.play()
                            new_position = old_position
                            
            if new_position.collidelistall(game.level_map.mobs): #collision with mobs
                for mob in game.level_map.mobs:
                    if mob.rect == new_position:
                        game.mob_hit_player.play()
                        self.gems -= mob.damage
                        self.score += 10
                        game.level_map.mobs.remove(mob)
                        
            
            if new_position.collidelistall(game.level_map.breakable): #breakable is a list of breakable walls, needed to seperate from regular walls
                for wall in game.level_map.breakable:
                    if wall.rect == new_position:
                        game.hit_wall.play()
                        new_position = old_position
                        
            if new_position.collidelistall(game.level_map.hidden_walls): # this is the hidden walls, maybe only level 1? when bumped it appears
                for wall in game.level_map.hidden_walls: 
                    if wall == new_position:
                        game.hit_wall.play()
                        new_position = old_position
                        game.level_map.walls.append(wall)
                
                
            if new_position.collidelistall(game.level_map.exits): #did they get to the level exit?
                for level_exit in game.level_map.exits:
                    if level_exit == new_position:
                        self.score += 50
                        game.level_map.level += 1
                        game.level_map.clearLevel()
                        RLmap.renderAll(game)
                        game.clock.tick(2)
                        game.level_map.makeMap(game)
                        game.level_map.panel.messages = []
                        RLmap.renderAll(game)
                        
                        '''while not pygame.event.wait().type in (QUIT, KEYDOWN):
                            pass'''
                        return
            if new_position.collidelistall(game.level_map.pits):
                anim.pitFall(game)
                
            if new_position.collidelistall(game.level_map.lava): #lava collision
                for lava in game.level_map.lava:
                    if lava.rect == new_position:
                        game.lava.play()
                        self.gems -= 10
                        game.level_map.lava.remove(lava)
                        game.level_map.floors.append(lava.rect)
            '''
             THIS SHOULD TAKE points away if player hits mobtile, however it only works if hitting a 
             space they used to be in. not working right obviosuly
             
            if new_position.collidelistall(game.level_map.moveable_walls):
                self.score -= 10
                new_position = old_position
                return'''
                        
            '''
            take this out to try and return position instwead
            self.rect = new_position

        else:
            game.hit_wall.play()
            self.rect = old_position'''
            
            position = new_position
        
        else:
            game.hit_wall.play()
            position = old_position
            
        return position    

        
    def whip(self, game):
        #if self.whip_frame >= 8:
            #whip_frame = 1
        
        if self.whips > 0:
            
            if self.whip_frame == 1:
                new_position = self.rect.move(0, -IMGSIZE)
                self.weapon.update(new_position, 1)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 2:
                new_position = self.rect.move(-IMGSIZE, -IMGSIZE)
                self.weapon.update(new_position, 2)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame += 1
                return
         
            if self.whip_frame == 3:
                new_position = self.rect.move(-IMGSIZE, 0)
                self.weapon.update(new_position, 3)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 4:
                new_position = self.rect.move(-IMGSIZE, IMGSIZE)
                self.weapon.update(new_position, 4)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 5:
                new_position = self.rect.move(0, IMGSIZE)
                self.weapon.update(new_position, 1)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 6:
                new_position = self.rect.move(IMGSIZE, IMGSIZE)
                self.weapon.update(new_position, 2)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame += 1
                return
            
            if self.whip_frame == 7:
                new_position = self.rect.move(IMGSIZE, 0)
                self.weapon.update(new_position, 3)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame += 1
                return
                
            if self.whip_frame == 8:
                new_position = self.rect.move(IMGSIZE, -IMGSIZE)
                self.weapon.update(new_position, 4)
                self.weapon.draw(game.surface)
                self.weapon.checkCollision(game)
                self.whip_frame = 1
                self.whips -= 1
                self.whipping = False
                return
           
        else:
            pass