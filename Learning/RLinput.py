import pygame
from pygame.locals import *

def getKeys():
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
            for a in RL.game.level_map.mobs:
                a.move(RL.game.player, RL.game.level_map)
        '''if event.type == game.timers['move_walls']:
            game.level_map.moveWalls(game)'''
        if event.type == USEREVENT+5:
            RL.game.level_map.lavaFlow(game)
        
