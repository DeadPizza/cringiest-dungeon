import pygame
from test import load_image
import random

# Комната занимает 1/3 экрана т.е 1280 / 3 = 430 по ширине
#                  2/3 т.е 720 / 3 * 2 = 480 (420) по высоте, 240 (300) - на инвентарь
class Map(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.img = load_image('backs/testmap.png')
        self.rect = self.img.get_rect()
        self.dx = 0
        self.moving = False
        self.heroes = None

    def set_heroes(self, h):
        self.heroes = h

    def update(self, *event):
        mpos = pygame.mouse.get_pos()
        #for event in events:
        flag = True
        for hero in self.heroes:
            if hero.rect.collidepoint(mpos): flag = False
        if event:
            if flag and event[0].type == pygame.MOUSEBUTTONDOWN:
                self.moving = True
            elif event[0].type == pygame.MOUSEBUTTONUP:
                self.moving = False

        if self.moving:
            self.dx -= 3 * (1 - 2 * (mpos[0] < 640))
            if self.dx > 0:
                self.dx = 0
            elif self.dx < -1650:
                self.dx = -1650

        self.screen.blit(self.img, (self.dx, 0))


class Inventory(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.img = load_image('backs/inventory_test.png')
        
    def update(self, *event):
        self.screen.blit(self.img, (0, 420))

class Hero(pygame.sprite.Sprite):
    def __init__(self, group, number, screen):
        super().__init__(group)
        self.screen = screen
        self.img = load_image('hero.png')
        self.img_2 = self.img#load_image('arrow.png')
        self.rect = self.img.get_rect()
        self.x = 10 + 120 * (number - 1)
        self.rect.topleft = self.x, 150
        self.HP, self.MAX_HP = 13, 13
        self.STRESS = 0
        self.myfont = pygame.font.SysFont('Arial', 20)

        self.is_active = False

    def update(self, *event):
        if not self.is_active:
            self.is_active = self.rect.collidepoint(pygame.mouse.get_pos()) and event and event[0].type == pygame.MOUSEBUTTONDOWN
            self.screen.blit(self.img, (self.x, 150))
        if self.is_active:
            if not self.rect.collidepoint(pygame.mouse.get_pos()) and event and event[0].type == pygame.MOUSEBUTTONDOWN:
                self.is_active = False
            textsurface = self.myfont.render(str(self.HP) + '/' + str(self.MAX_HP), False, (255, 0, 0))
            self.screen.blit(textsurface, (106, 543))
            textsurface = self.myfont.render(str(self.STRESS), False, (255, 255, 255))
            self.screen.blit(textsurface, (106, 566))
            self.screen.blit(self.img_2, (self.x, 150))

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
    mp = Map(target_sprite_group, screen)
    Inventory(target_sprite_group, screen)
    h1 = Hero(target_sprite_group, 1, screen)
    h1.HP = 10
    h2 = Hero(target_sprite_group, 2, screen)
    h2.HP = 11
    h3 = Hero(target_sprite_group, 3, screen)
    h3.HP = 12
    h4 = Hero(target_sprite_group, 4, screen)
    h4.HP = 13
    heroes = [h1, h2, h3, h4]
    mp.set_heroes(heroes)
    #while True:
    #    target_sprite_group.update(pygame.event.get())
    #    screen.blit(update_fps(), (10,0))
    #    pygame.display.flip()
    #    clock.tick()
    while True:
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            target_sprite_group.update(event)
        if not events:
            target_sprite_group.update()
        screen.blit(update_fps(), (5, 5))
        pygame.display.flip()
        clock.tick()