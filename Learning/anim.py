import os,sys
from RLCONSTANTS import WWIDTH, WHEIGHT, IMGSIZE, IMGDIR, DARKFLOOR, DARKWALL, images
import RLobject
import RLmap

import pygame
from pygame.locals import *



def intro(surface):
    surface.fill((0,0,0))
    pygame.display.update()
    pygame.event.wait()
    while not pygame.event.wait().type in (QUIT, KEYDOWN):
        pass
    return


def pitFall(game):
    game.level_map.clearLevel() # this gets rid of all the walls and what not so player can fall all normal like
    width = WWIDTH / IMGSIZE
    height = WHEIGHT / IMGSIZE
    screens_fell = 0
    game.player.rect.top = 0
    game.player.rect.left = 520
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        game.surface.fill((0,0,0))
        for a in range(len(game.level_map.level_map)):
            print(len(game.level_map.level_map))
            for b in range(len(game.level_map.level_map[a])):
                y = a * IMGSIZE # this sets the x and y coords by the number of pixels the image is, 16 ,32 etc.
                x = b * IMGSIZE
                if x < 496 or x > 544:
                    game.surface.blit(images['wall'], (x,y))
            
        game.player.move(0,IMGSIZE, game)
        game.player.draw(game.surface)
        pygame.display.update()
        if game.player.rect.top > 368:
            game.player.rect.top = 0
            screens_fell +=1
        if screens_fell == 5:
            for x in range(len(game.level_map.level_map[-1])):
                game.surface.blit(images['wall'], (x,368))
        if screens_fell > 5:
            break
             
        game.clock.tick(10)
    gameOver(game)
    
        
    
 

def gameOver(game):

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_y:
                    game.player = RLobject.Player(os.path.join(IMGDIR, 'player.bmp'), 0, 0)
                    game.level_map = RLmap.Map(1, game.player)
                    return
                if event.key == K_n:
                    game.game_over = True
                    return
        game.surface.fill((0,0,0)) 
        game_over =  game.font.render('GAME OVER!', True, DARKFLOOR)
        play_again =  game.font.render('Play again? (y/n)', True, DARKFLOOR)
        game.surface.blit(game_over, (WWIDTH /2, WHEIGHT / 2))
        game.surface.blit(play_again, (WWIDTH / 2, WHEIGHT / 2 + 10))
        pygame.display.update()
   
   

    
           


      
    
