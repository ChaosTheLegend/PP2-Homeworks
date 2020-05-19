import os
from pathlib import Path
import pygame
import colorsys

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

#image loader:
imgdir = Path(__file__).parent
imgdir = os.path.join(imgdir,Path('images'))

def LoadImage(name):
    return pygame.image.load(os.path.join(imgdir,Path(name)))

#sound loader
soundir = Path(__file__).parent
soundir = os.path.join(soundir,Path('sounds'))
 
def LoadSound(name):
    sndfl =  (os.path.join(soundir,Path(name)))
    return pygame.mixer.Sound(sndfl)

