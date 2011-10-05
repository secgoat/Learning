import sys, os, math
import pygame
from RLobject import *
from RLCONSTANTS import *
import RLmap, RLinput
import anim
from pygame.locals import *



class Game:
    def __init__(self):
        self.level = 0
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)
        pygame.display.set_caption('Zero Trunk Rot')
        self.player = Player(os.path.join(IMGDIR, 'player.bmp'), 0, 0)
        self.level_map = RLmap.Map(1, self)
        self.font = pygame.font.Font(os.path.join(RESDIR,'visitor1.ttf'),18)
        self.title_font = pygame.font.Font(os.path.join(RESDIR,'visitor1.ttf'),36)
        self.game_over = False
        self.setTimers()
        self.setSounds()
        
    def setSounds(self):
        
        self.mob_hit_player = pygame.mixer.Sound(os.path.join(RESDIR, 'mobHitPlayer.wav'))
        self.currentVolume = 1.0
        self.musicPause = False
        pygame.mixer.music.set_volume(self.currentVolume)

        

    def checkState(self):
        if self.player.gems < 1:
            #self.game_over = True
            anim.gameOver(game)
        #else:
            #return
    def setTimers(self):
        pygame.time.set_timer(slow, SLOW) # movement for slow enemies every time this goes off slow enemies are allowed to move
        pygame.time.set_timer(medium, MEDIUM) #medium movement
        pygame.time.set_timer(fast, FAST) #fast movement
        pygame.time.set_timer(lava, OFF) #lava flow
        pygame.time.set_timer(check_things, OFF)
        
    def changeTimer(self, timer, speed):
        pygame.time.set_timer(timer, speed)
        
    def slowTimers(self):
        pygame.time.set_timer(slow, SLOW + 500) # movement for slow enemies every time this goes off slow enemies are allowed to move
        pygame.time.set_timer(medium, MEDIUM + 500) #medium movement
        pygame.time.set_timer(fast, FAST + 500) #fast movement
        
    def speedTimers(self):
        pygame.time.set_timer(slow, SLOW - 500) # movement for slow enemies every time this goes off slow enemies are allowed to move
        pygame.time.set_timer(medium, MEDIUM - 500) #medium movement
        pygame.time.set_timer(fast, FAST - 500) #fast movement

    def stopTimers(self):
        pygame.time.set_timer(slow, OFF) # movement for slow enemies every time this goes off slow enemies are allowed to move
        pygame.time.set_timer(medium, OFF) #medium movement
        pygame.time.set_timer(fast, OFF) #fast movement
                    
    def showMenu(self):
        pass

    def isInRange(self, center_x, center_y, radius, x, y):
        square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
        return square_dist <= radius ** 2
    
    
    



#pygame initialization
pygame.init()


    
    
game = Game()
anim.intro(game)

while not game.game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit('You quit!')
        if event.type == KEYDOWN:
            if event.key == K_KP7:
                game.player.move(-IMGSIZE, -IMGSIZE, game)
            if event.key == K_KP9:
                game.player.move(IMGSIZE, -IMGSIZE, game)
            if event.key == K_KP1:
                game.player.move(-IMGSIZE, IMGSIZE, game)
            if event.key == K_KP3:
                game.player.move(IMGSIZE, IMGSIZE, game)   
            if event.key == K_LEFT or event.key == K_KP4:
                game.player.move(-IMGSIZE, 0, game)
            if event.key == K_RIGHT or event.key == K_KP6:
                game.player.move(IMGSIZE, 0, game)
            if event.key == K_UP or event.key == K_KP8:
                game.player.move(0, -IMGSIZE, game)
            if event.key == K_DOWN or event.key == K_KP2:
                game.player.move(0, IMGSIZE, game)
            if event.key == K_t:
                if game.player.teleports > 0:
                    game.player.teleport(game)
            if event.key == K_x:
                game.player.keys += 10
                game.player.teleports += 10
                game.player.whips += 10
                game.player.gems += 10
            if event.key == K_m:
                game.player.findMovingWalls(game)
                game.changeTimer(lava, VERYSLOW)
                #print(game.level_map.moveable_walls)   
            if event.key == K_n:
                game.level_map.level += 1
                game.level_map.clearLevel()
                RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
                game.clock.tick(2)
                game.level_map.makeMap(game)
                RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
                while not pygame.event.wait().type in (QUIT, KEYDOWN):
                    pass
            if event.key == K_SPACE:
                if game.player.whips > 0:
                    game.player.whipping = True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        #if event.type == USEREVENT+1:
        if event.type == slow:
            for a in game.level_map.mobs:
                a.move(game)
            for wall in game.level_map.moveable_walls:
                if wall.moving == True:
                    wall.move(game)
        '''if event.type == game.timers['move_walls']:
            game.level_map.moveWalls(game)'''
        if event.type == lava:
            game.level_map.lavaFlow(game)
        if event.type == check_things:
            #game.changeTimer(slow, SLOW)
            #game.changeTimer(check_things, OFF)
            game.setTimers()
            game.player.invisible = False


    RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
    game.checkState()
    game.clock.tick(16)



