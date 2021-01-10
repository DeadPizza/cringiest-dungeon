import os
import sys
import pygame
import random


def load_image(name, colorkey=None):
        fullname = os.path.join('resources/images', name)
        if not os.path.isfile(fullname):
            print(f"file '{fullname}' not found")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

def load_audio(name):
    fullname = os.path.join('resources/audio', name)
    if not os.path.isfile(fullname):
            print(f"file '{fullname}' not found")
            sys.exit()
    return pygame.mixer.Sound(fullname)