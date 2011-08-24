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


#set up the player
player = Player('player.bmp', 480, 288)
mob = Mob('a.bmp', 304, 288)
#map
testMap = RLmap.Map()
testMap.mobs.append(mob)
UPDATE = pygame.USEREVENT
pygame.time.set_timer(UPDATE, int(1000.0/30))
#while True:
while player.gems > 0:
    for event in pygame.event.get():
        pass
        
            
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
    
                corner_x = player.rect.right
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
                print('Rect:{0}\n Gems:{1} \n Whips:{2}\n'.format(player.rect, player.gems, player.whips))
            if event.key == K_SPACE:
                player.whipping = True
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
    
        
    RLmap.renderAll(basicFont, windowSurface, testMap, images, player)
    for a in testMap.mobs:
        a.move(player, testMap)
    mainClock.tick(1)
                 
