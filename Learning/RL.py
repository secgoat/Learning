import sys, os
import pygame
from RLobject import *
from RLCONSTANTS import *
import RLmap, RLinput
import anim
from pygame.locals import *

''' //TODO:
1. make mobs break or remove items when stepping on them  - DONE
2. Make mobs less sensitive to player, only move when in same room, or on trigger spaces
3. colleciton of K R O Z letters
4. Lava: remove 10 gems and the lava square, Lava expands DONE
5. Whip Power Ring - DONE
6. Bottomless Pits
7. Spells:6
    Freeze Creature
    slow creature
    image for teleport trap - DONE
    earthquake (adds bolders)
    invisibility
8. wait for player to press key to start level - DONE
9. moving walls
10. Bomb
11. the ? (not sure what it is yet)
12. ancient tablets
13. the randomly generated levels
14. figure out the differences between mobs, so far i have 3 timers set up, need to at least make them move at different speeds
15. add the 32x32 tiles and figure out how to scroll map
16. sound
17. splash / animation screens
        title
        death
        pit
        highscore
        
'''

class Game:
    def __init__(self):
        self.level = 0
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)
        pygame.display.set_caption('Rokz Return')
        self.player = Player(os.path.join(IMGDIR, 'player.bmp'), 0, 0)
        self.level_map = RLmap.Map(3, self.player)
        self.font = pygame.font.Font(None,24)
        self.game_over = False
        self.timers = {}
        self.setTimers()
        
    def checkState(self):
        if self.player.gems < 1:
            self.game_over = True
            #anim.gameOver(game.game_over)
        #else:
            #return
    def setTimers(self):
        self.timers['slow'] = pygame.time.set_timer(USEREVENT+1, 1000) # movement for slow enemies every time this goes off slow enemies are allowed to move
        self.timers['medium'] = pygame.time.set_timer(USEREVENT+2, 750) #medium movement
        self.timers['fast'] = pygame.time.set_timer(USEREVENT+3, 500) #fast movement
        self.timers['move_walls'] = ' '
        
        
#pygame initialization
pygame.init()

game = Game()
anim.intro(game.surface)


pygame.time.set_timer(USEREVENT+1, 1000) # movement for slow enemies every time this goes off slow enemies are allowed to move
pygame.time.set_timer(USEREVENT+2, 750) #medium movement
pygame.time.set_timer(USEREVENT+3, 500) #fast movement
pygame.time.set_timer(USEREVENT+5, 500) #lava flow

while not game.game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit('You quit!')
        if event.type == KEYDOWN:
            if event.key == K_KP7:
                game.player.move(-IMGSIZE,-IMGSIZE, game)
            if event.key == K_KP9:
                game.player.move(IMGSIZE,-IMGSIZE, game)
            if event.key == K_KP1:
                game.player.move(-IMGSIZE,IMGSIZE, game)
            if event.key == K_KP3:
                game.player.move(IMGSIZE,IMGSIZE, game)   
            if event.key == K_LEFT or event.key == K_KP4:
                game.player.move(-IMGSIZE,0, game)
            if event.key == K_RIGHT or event.key == K_KP6:
                game.player.move(IMGSIZE,0, game)
            if event.key == K_UP or event.key == K_KP8:
                game.player.move(0,-IMGSIZE, game)
            if event.key == K_DOWN or event.key == K_KP2:
                game.player.move(0,IMGSIZE, game)
            if event.key == K_t:
                game.player.teleport(game)
            if event.key == K_x:
                game.player.keys += 10
                game.player.teleports += 10
                game.player.whips += 10
                game.player.gems += 10
                #print('Rect:{0}\n Gems:{1} \n Whips:{2}\n player:{3}'.format(game.player.rect, game.player.gems, game.player.whips, game.player))
                print(game.level_map.exits)
            if event.key == K_n:
                game.level_map.level += 1
                game.level_map.clearLevel()
                RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
                game.clock.tick(2)
                game.level_map.makeMap(game.player)
                RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
                while not pygame.event.wait().type in (QUIT, KEYDOWN):
                    pass
            if event.key == K_SPACE:
                game.player.whipping = True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        if event.type == USEREVENT+1:
            for a in game.level_map.mobs:
                a.move(game.player, game.level_map)
        if event.type == game.timers['move_walls']:
            game.level_map.moveWalls(game)
        if event.type == USEREVENT+5:
            game.level_map.lavaFlow(game)
            

    RLmap.renderAll(game.font, game.surface, game.level_map, images, game.player)
    game.checkState()
    game.clock.tick(16)


                 
