import os
import sys
import pygame

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('resources', name)
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

all_sprites = pygame.sprite.Group()
bomb = pygame.sprite.Sprite(all_sprites)
bomb.image = load_image('test.png')
bomb.rect = bomb.image.get_rect()
bomb.rect.x = 100
bomb.rect.y = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bomb.rect = bomb.rect.move(0, 10)

    all_sprites.draw(screen)
    pygame.display.flip()