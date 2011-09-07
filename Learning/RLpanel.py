from RLCONSTANTS import *
import pygame
from pygame.locals import *
class Panel:
    
    def __init__(self):
        self.messages = []
        
        
    def update(self, player, font, level_map):
        self.messages.reverse()
        if len(self.messages) > 8:
            self.messages.pop()
        y = 410
        for message in range(len(self.messages)):
            y += 20
            display_msg = font.render(self.messages[message], True, DARKFLOOR)
            windowSurface.blit(display_msg, (160, y))
            
        self.messages.reverse()
        
        level = font.render(str(level_map.level), True, DARKFLOOR)
        score = font.render(str(player.score), True, DARKFLOOR)
        whips = font.render(str(player.whips), True, DARKFLOOR)
        gems = font.render(str(player.gems), True, DARKFLOOR)
        teleports = font.render(str(player.teleports), True, DARKFLOOR)
        keys =  font.render(str(player.keys), True, DARKFLOOR)
        
        levelTitle = font.render('Level: ', True, DARKFLOOR)
        scoreTitle = font.render('Score: ', True, DARKFLOOR)
        whipTitle = font.render('Whips: ', True, DARKFLOOR)
        gemTitle = font.render('Gems: ', True, DARKFLOOR)
        teleportTitle = font.render('Teles: ', True, DARKFLOOR)
        keyTitle = font.render('Keys: ', True, DARKFLOOR)
        
        windowSurface.blit(levelTitle, (20, 420))
        windowSurface.blit(level,(80,420))
        windowSurface.blit(scoreTitle, (20, 440))
        windowSurface.blit(score, (80, 440))
        
        windowSurface.blit(whipTitle, (20, 460))
        windowSurface.blit(whips, (80, 460))
        
        windowSurface.blit(gemTitle, (20, 480))
        windowSurface.blit(gems, (80, 480))
        
        windowSurface.blit(teleportTitle, (20, 500))
        windowSurface.blit(teleports, (80, 500))
        
        windowSurface.blit(keyTitle, (20, 520))
        windowSurface.blit(keys, (80, 520))
        
    
        pygame.draw.rect(windowSurface, DARKWALL, (10, 410 ,1038, 200), 6)
        pygame.draw.rect(windowSurface, DARKWALL, (140, 410, 910, 200), 6)
        