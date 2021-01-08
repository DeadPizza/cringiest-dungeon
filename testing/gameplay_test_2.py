from test import load_image
import pygame
import json


class Hero:
    def __init__(self, sprite, number):
        self.x = 10 + 120 * (number - 1)

        self.image = load_image(sprite)
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, 150)

        self.HP, self.MAX_HP = 100, 100
        self.STRESS = 10


class Inventory:
    def __init__(self, sprite):
        self.image = load_image(sprite)


class BattleController:
    def __init__(self, screen):
        self.screen = screen

        self.heroes = load_heroes((0, 1, 2, 3))
        self.hero_current = None
        self.hero_UI_font = pygame.font.SysFont('Arial', 20)

        self.map_image = load_image('backs/testmap.png')
        self.map_image_rect = self.map_image.get_rect()
        self.map_dx = 0
        self.map_moving = False

        self.inventory = Inventory('backs/inventory_test.png')

    def update(self):
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.onClickDown(mpos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.onClickUp()

        if self.map_moving:
            self.map_dx -= 1
            self.map_dx -= 3 * (1 - 2 * (mpos[0] < 640))
            if self.map_dx > 0:
                self.map_dx = 0
            elif self.map_dx < -1650:
                self.map_dx = -1650

        self.screen.blit(self.map_image, (self.map_dx, 0))
        self.screen.blit(self.inventory.image, (0, 420))
        for hero in self.heroes:
            self.screen.blit(hero.image, (hero.x, 150))

        if self.hero_current is not None:
            textsurface = self.hero_UI_font.render(str(self.hero_current.HP) + '/' + str(self.hero_current.MAX_HP), False, (255, 0, 0))
            self.screen.blit(textsurface, (106, 543))
            textsurface = self.hero_UI_font.render(str(self.hero_current.STRESS), False, (255, 255, 255))
            self.screen.blit(textsurface, (106, 566))

    def onClickDown(self, mpos):
        index = self.checkHeroes(mpos)
        if index:
            self.hero_current = self.heroes[index - 1]
        else:
            self.hero_current = None
            if self.map_image_rect.collidepoint(mpos):
                self.map_moving = True

    def onClickUp(self):
        self.map_moving = False

        
    def checkHeroes(self, mpos):
        for index in range(4):
            if self.heroes[index].image_rect.collidepoint(mpos):
                return index + 1
        return 0


def load_heroes(indexes):
    f = open('save/heroes.json') 
    saved_data = json.load(f)
    heroes = []
    for j, i in enumerate(indexes):
        hero_loaded = saved_data[i]
        sprite = hero_loaded['texture']
        heroes.append(Hero(sprite, j + 1))
    f.close()
    return heroes


if __name__ == '__main__':
    from settings import *
    pygame.init()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    trg = BattleController(screen)

    font = pygame.font.SysFont("Arial", 18)
    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text
    
    while True:
        screen.fill((0, 0, 0))
        trg.update()
        screen.blit(update_fps(), (5, 5))
        pygame.display.flip()
        clock.tick()