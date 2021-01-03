import pygame
from test import load_image

# Комната занимает 1/3 экрана т.е 1280 / 3 = 430 по ширине
#                  2/3 т.е 720 / 3 * 2 = 480 (420) по высоте, 240 (300) - на инвентарь

class Map(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.img = load_image('testmap.png')
        self.dx = 0
        self.moving = False

    def update(self, *event):
        if event:
            if event[0].type == pygame.MOUSEBUTTONDOWN:
                self.moving = True
            elif event[0].type == pygame.MOUSEBUTTONUP:
                self.moving = False

        if self.moving:
            self.dx -= 3 * (1 - 2 * (pygame.mouse.get_pos()[0] < 640))
            if self.dx > 0:
                self.dx = 0
            elif self.dx < -1650:
                self.dx = -1650

        self.screen.blit(self.img, (self.dx, 0))


class Inventory(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.img = load_image('inventory_test.png')
        
    def update(self, *event):
        self.screen.blit(self.img, (0, 420))

class Hero(pygame.sprite.Sprite):
    def __init__(self, group, number, screen):
        super().__init__(group)
        self.screen = screen
        self.img = load_image('hero.png')
        self.x = 10 + 120 * (number - 1)

    def update(self, *event):
        self.screen.blit(self.img, (self.x, 150))

if __name__ == '__main__':
    from settings import *
    pygame.init()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)


    font = pygame.font.SysFont("Arial", 18)
    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    target_sprite_group = pygame.sprite.Group()
    Map(target_sprite_group, screen)
    Hero(target_sprite_group, 1, screen)
    Hero(target_sprite_group, 2, screen)
    Hero(target_sprite_group, 3, screen)
    Hero(target_sprite_group, 4, screen)
    Inventory(target_sprite_group, screen)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            target_sprite_group.update(event)
        if not events:
            target_sprite_group.update()
        screen.blit(update_fps(), (10,0))
        pygame.display.flip()
        clock.tick(FPS)