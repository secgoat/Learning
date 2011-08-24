import sys
import random
from random import choice
import math
import pygame
from pygame.locals import *


#Game Window variables 
WWIDTH = 1056
WHEIGHT = 616

#Image Variables
IMGSIZE = 16

#map scrolling variables
view_width = 768
view_height = 800
scroll_dx = IMGSIZE
scroll_dy = IMGSIZE
corner_x = 0
corner_y = 0


#Surface
windowSurface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)
windowSurface.convert()
#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKWALL = (0,0,100)
DARKFLOOR = (50,50,150)


#Images
wallImage = pygame.image.load('wall.bmp').convert_alpha()
floorImage = pygame.image.load('floor.bmp').convert_alpha()
waterImage = pygame.image.load('water.bmp').convert_alpha()
breakableWall = pygame.image.load('breakable.bmp').convert_alpha()
stairsImage = pygame.image.load('stairs.bmp').convert_alpha()
images = {'wall':wallImage, 'floor':floorImage, 'water':waterImage, 'breakable':breakableWall, 'stairs':stairsImage}
