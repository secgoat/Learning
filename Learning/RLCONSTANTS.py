import sys
import random
import pygame
from pygame.locals import *

#Game Window variables 
WWIDTH = 1024
WHEIGHT = 768

#Image Variables
IMGSIZE = 32

#Surface
windowSurface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)
#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKWALL = (0,0,100)
DARKFLOOR = (50,50,150)


#Images
wallImage = pygame.image.load('wall.bmp').convert_alpha()
floorImage = pygame.image.load('floor.bmp').convert_alpha()
images = {'wall':wallImage, 'floor':floorImage}
