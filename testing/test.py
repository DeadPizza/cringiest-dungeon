import os
import sys
import pygame
import random


def load_image(name, colorkey=None):
        fullname = os.path.join('resources/photo', name)
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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    class Bomb(pygame.sprite.Sprite):
        image = load_image("bomb.png")

        def __init__(self, *group):
            super().__init__(*group)
            self.image = Bomb.image
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(width)
            self.rect.y = random.randrange(height)

        def update(self):
            self.rect = self.rect.move(random.randrange(3) - 1, 
                                    random.randrange(3) - 1)
                                    
    for _ in range(50):
        Bomb(all_sprites)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        screen.fill((255, 255, 255))