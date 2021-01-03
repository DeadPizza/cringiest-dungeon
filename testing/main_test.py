import pygame
from test import load_image
from settings import *
from gameplay_test import Inventory, Map, Hero


pygame.init()
clock = pygame.time.Clock()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

def set_game_stage(stage):
    global target_sprite_group
    target_sprite_group = pygame.sprite.Group()
    if stage == 'menu':
        MainMenuPicture(target_sprite_group, screen)
        StartGame(target_sprite_group, screen)
        Cursor(target_sprite_group, screen)
    elif stage == 'test':
        Shit(target_sprite_group, screen)
        Cursor(target_sprite_group, screen)
    elif stage == 'battle':
        Map(target_sprite_group, screen)
        Hero(target_sprite_group, 1, screen)
        Hero(target_sprite_group, 2, screen)
        Hero(target_sprite_group, 3, screen)
        Hero(target_sprite_group, 4, screen)
        Inventory(target_sprite_group, screen)
        Cursor(target_sprite_group, screen)

class Cursor(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        pygame.mouse.set_visible(False)
        self.img = load_image('arrow.png')
        self.rect = self.img.get_rect()

    def update(self, *event):
        if pygame.mouse.get_focused():
            self.rect.center = pygame.mouse.get_pos()
            self.screen.blit(self.img, self.rect)


class MainMenuPicture(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.music = pygame.mixer.Sound('resources/audio/mm_music.mp3')
        self.img = load_image('bg_main_menu.png')
        self.music.play()

    def update(self, *event):
        self.screen.blit(self.img, (0, 0))


class StartGame(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.img_idle = load_image('button_main_menu_start_idle.png')
        self.img_hovered = load_image('button_main_menu_start_hovered.png')
        self.rect = self.img_idle.get_rect()

        self.image = self.img_idle

    def update(self, *event):
        self.rect.center = 640, 550
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.img_hovered
            if event and event[0].type == pygame.MOUSEBUTTONDOWN:
                set_game_stage('battle')
        else:
            self.image = self.img_idle

        self.screen.blit(self.image, self.rect)


class Shit(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__(group)
        self.screen = screen
        self.img = load_image('lulza.jpg')

    def update(self, *event):
        self.screen.blit(self.img, (0, 0))

target_sprite_group = pygame.sprite.Group()
set_game_stage('menu')

font = pygame.font.SysFont("Arial", 18) 
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text

while True:
    screen.fill((0, 0, 0))
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