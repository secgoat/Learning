import os,sys
from RLCONSTANTS import WWIDTH, WHEIGHT, IMGSIZE, IMGDIR, RESDIR, DARKFLOOR, DARKWALL, images
import RLobject
import RLmap

import pygame
from pygame.locals import *



def intro(game):
    
    
    ret = game.title_font.render('Return', True, DARKFLOOR)
    to =  game.title_font.render('To', True, DARKFLOOR)
    kroz = game.title_font.render('Kroz', True, DARKFLOOR)
    start= game.font.render('Start Game', True, DARKFLOOR)
    instructions = game.font.render('How To Play', True, DARKFLOOR)
    quit_option = game.font.render('Quit', True, DARKFLOOR)
    selector = game.font.render('>', True, DARKFLOOR)
    select_pos = [(WWIDTH /2 - 10, WHEIGHT /3 + 138),(WWIDTH /2 - 10, WHEIGHT /3 + 156),(WWIDTH /2 - 10,WHEIGHT / 3 + 174)]
    pos = 0
    game.surface.blit(ret, (WWIDTH / 2, WHEIGHT / 3))
    game.surface.blit(to, (WWIDTH / 2 , WHEIGHT / 3 + 36))
    game.surface.blit(kroz, (WWIDTH / 2, WHEIGHT / 3 + 72))
    game.surface.blit(start, (WWIDTH /2, WHEIGHT / 3 + 138))
    game.surface.blit(instructions,(WWIDTH /2, WHEIGHT /3 + 156))
    game.surface.blit(quit_option, (WWIDTH /2, WHEIGHT / 3 + 174))
    
    game.surface.blit(selector, (WWIDTH /2 - 10, WHEIGHT /3 + 138))
    
    pygame.event.wait()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_UP or event.key == K_w or event.key == K_KP8:
                    pos -= 1
                    if pos < 0:
                        pos = 2
                if event.key == K_DOWN or event.key == K_s or event.key == K_KP2:
                    pos += 1
                    if pos > 2:
                        pos = 0
                if event.key == K_RETURN or event.key == K_SPACE:
                    if pos == 0:
                        return
                    if pos == 1:
                        displayInstructions(game)
                        return
                    if pos == 2:
                        pygame.quit()
                        sys.exit()  
                        
        game.surface.fill((0,0,0))
        game.surface.blit(ret, (WWIDTH / 2, WHEIGHT / 3))
        game.surface.blit(to, (WWIDTH / 2 , WHEIGHT / 3 + 36))
        game.surface.blit(kroz, (WWIDTH / 2, WHEIGHT / 3 + 72))
        game.surface.blit(start, (WWIDTH /2, WHEIGHT / 3 + 138))
        game.surface.blit(instructions,(WWIDTH /2, WHEIGHT /3 + 156))
        game.surface.blit(quit_option, (WWIDTH /2, WHEIGHT / 3 + 174))
        game.surface.blit(selector, select_pos[pos])
        pygame.display.update()            
    '''while not pygame.event.wait().type in (QUIT, KEYDOWN):
        pass'''
    return

def displayInstructions(game):
    game.surface.fill((0,0,0))
    f = open(os.path.join(RESDIR,'howto.txt'),'r')
    lines = f.readlines()
    font_height = game.font.get_height()
    surfaces = [game.font.render(ln, True, DARKFLOOR) for ln in lines]
    #maxwidth = max([s.get_width() for s in surfaces])
    #result = pygame.Surface((maxwidth, len(lines)*font_height), pygame.SRCALPHA)
    while True:
        for i in range(len(lines)):
            game.surface.blit(surfaces[i], (100,i*font_height))
            
        pygame.display.update()
    
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
        game.surface.blit(play_again, (WWIDTH / 2, WHEIGHT / 2 + 20))
        pygame.display.update()
   
   

    
           


      
    
