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
pygame.time.set_timer(USEREVENT+1, 1000) # movement for slow enemies everytiem this goes off slow enemies are allowed to move
pygame
pygame.display.set_caption('RogueLike Test')
basicFont = pygame.font.Font(None,24)


#set up the player
player = Player('player.bmp', 0, 0)

#map
testMap = RLmap.Map(1, player)

#while True:
while player.gems > 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit('You quit!')
        if event.type == KEYDOWN:
            if event.key == K_KP7:
                player.move(-IMGSIZE,-IMGSIZE, testMap)
            if event.key == K_KP9:
                player.move(IMGSIZE,-IMGSIZE, testMap)
            if event.key == K_KP1:
                player.move(-IMGSIZE,IMGSIZE, testMap)
            if event.key == K_KP3:
                player.move(IMGSIZE,IMGSIZE, testMap)
                
            if event.key == K_LEFT or event.key == K_KP4:
                player.move(-IMGSIZE,0, testMap)
            if event.key == K_RIGHT or event.key == K_KP6:
                player.move(IMGSIZE,0, testMap)
            if event.key == K_UP or event.key == K_KP8:
                player.move(0,-IMGSIZE, testMap)
            if event.key == K_DOWN or event.key == K_KP2:
                player.move(0,IMGSIZE, testMap)
            if event.key == K_t:
                player.teleport(testMap)
            if event.key == K_x:
                player.keys += 10
                player.teleports += 10
                player.whips += 10
                print('Rect:{0}\n Gems:{1} \n Whips:{2}\n'.format(player.rect, player.gems, player.whips))
            if event.key == K_SPACE:
                player.whipping = True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        if event.type == USEREVENT+1:
            for a in testMap.mobs:
                a.move(player, testMap)
            
    
        
    RLmap.renderAll(basicFont, windowSurface, testMap, images, player)
    mainClock.tick(16)
                 
