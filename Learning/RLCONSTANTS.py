import os
import pygame
from pygame.locals import *

#paths
if os.name =='posix':
    #LINUX
    ROOTDIR = os.path.abspath(os.curdir).replace(';','')
else:
    #WINDOWS
    ROOTDIR = os.getcwd().replace(';','')

IMGDIR = os.path.join(ROOTDIR, 'img')
LVLDIR = os.path.join(ROOTDIR, 'lvl')
RESDIR = os.path.join(ROOTDIR, 'res')


#Game Window variables 
WWIDTH = 1056
WHEIGHT = 616

#Image Variables
IMGSIZE = 16

#Timer speeds in milliseconds 0 = off
OFF = 0
ETERNITY = 10000
VERYSLOW = 2000
SLOW = 1000
MEDIUM = 750
FAST = 500


slow = USEREVENT+1
medium = USEREVENT+2
fast = USEREVENT+3
lava = USEREVENT+4
check_things = USEREVENT+5

#Surface
windowSurface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKWALL = (0,0,100)
DARKFLOOR = (50,50,150)

#Images
wallImage = pygame.image.load(os.path.join(IMGDIR,'wall.bmp')).convert_alpha()
floorImage = pygame.image.load(os.path.join(IMGDIR,'floor.bmp')).convert_alpha()
waterImage = pygame.image.load(os.path.join(IMGDIR,'water.bmp')).convert_alpha()
breakableWall = pygame.image.load(os.path.join(IMGDIR,'breakable.bmp')).convert_alpha()
stairsImage = pygame.image.load(os.path.join(IMGDIR,'stairs.bmp')).convert_alpha()
waterImage = pygame.image.load(os.path.join(IMGDIR,'water.bmp')).convert_alpha()
images = {'wall':wallImage, 'floor':floorImage, 'water':waterImage, 'breakable':breakableWall, 'stairs':stairsImage, 'water':waterImage}
