

def getKeys():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                playe['x'] -= 1
            if event.key == K_RIGHT:
                player['x'] += 1
            if event.key == K_UP:
                player['y'] -= 1
            if event.key == K_DOWN:
                player['y'] += 1
        
