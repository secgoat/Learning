from RLCONSTANTS import *


def update(player, font):
    
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
    
    windowSurface.blit(levelTitle, (862, 10))

    windowSurface.blit(scoreTitle, (785, 30))
    windowSurface.blit(score, (845, 30))
    
    windowSurface.blit(whipTitle, (785, 50))
    windowSurface.blit(whips, (845, 50))
    
    windowSurface.blit(gemTitle, (785, 70))
    windowSurface.blit(gems, (845, 70))
    
    windowSurface.blit(teleportTitle, (785, 90))
    windowSurface.blit(teleports, (845, 90))
    
    windowSurface.blit(keyTitle, (785, 110))
    windowSurface.blit(keys, (845, 110))
    
    
    pygame.draw.rect(windowSurface, DARKWALL, (782, 5 ,225, 763), 6)
    
    messages = []