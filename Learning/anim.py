from RLCONSTANTS import WWIDTH, WHEIGHT, IMGSIZE
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


def pit_fall():
    width = WWIDTH / IMGSIZE
    height = WHEIGHT / IMGSIZE
    for a in(len(width)):
        for b in (len(height)):
            surface.blit(images['breakable'], a, b)
    surface.fill((0,0,0))
    
    pass

def gameOver(game_over):
    game_over = True
    
