#import sys
#import pygame
from RLobject import *
from RLCONSTANTS import *
import RLmap
import RLpanel
#from pygame.locals import *

#pygame initialization
pygame.init()
mainClock = pygame.time.Clock()

#windowSurface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)
#pygame.Surface.set_colorkey(windowSurface, (71,108,108))
windowSurface.set_colorkey((71,108,108))
pygame.display.set_caption('RogueLike Test')
basicFont = pygame.font.Font(None,24)

#Images
#wallImage = pygame.image.load('wall.bmp').convert_alpha()
#floorImage = pygame.image.load('floor.bmp').convert_alpha()
#images = {'wall':wallImage, 'floor':floorImage}

#set up the player
player = Player('player.bmp', 32, 32)

#map
testMap = RLmap.Map()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit('You quit!')
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.move(-IMGSIZE,0, testMap)
            if event.key == K_RIGHT:
                player.move(IMGSIZE,0, testMap)
            if event.key == K_UP:
                player.move(0,-IMGSIZE, testMap)
            if event.key == K_DOWN:
                player.move(0,IMGSIZE, testMap)
            if event.key == K_x:
                print('Rect:{0}\n Gems:{1} \n Whips:{2}\n'.format(player.rect, player.gems, player.whips))
            if event.key == K_SPACE:
                player.whipping = True
                #player.whip(windowSurface, player.rect)
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    RLmap.renderAll(basicFont, windowSurface, testMap, images, player)
    
    mainClock.tick(40)
                    
