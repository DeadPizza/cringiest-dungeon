import pygame
from test import load_image


pygame.init()
clock = pygame.time.Clock()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

def set_game_stage(stage):
    global target_sprite_group
    target_sprite_group = pygame.sprite.Group()
    if stage == 'menu':
        MainMenuPicture(target_sprite_group)
        StartGame(target_sprite_group)
        Cursor(target_sprite_group)
    elif stage == 'test':
        Shit(target_sprite_group)
        Cursor(target_sprite_group)

class Cursor(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        pygame.mouse.set_visible(False)
        self.img = load_image('arrow.png')
        self.rect = self.img.get_rect()

    def update(self, *event):
        if pygame.mouse.get_focused():
            self.rect.center = pygame.mouse.get_pos()
            screen.blit(self.img, self.rect)


class MainMenuPicture(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.music = pygame.mixer.Sound('resources/audio/mm_music.mp3')
        self.img = load_image('bg_main_menu.png')
        self.music.play()

    def update(self, *event):
        screen.blit(self.img, (0, 0))


class StartGame(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.img_idle = load_image('button_main_menu_start_idle.png')
        self.img_hovered = load_image('button_main_menu_start_hovered.png')
        self.rect = self.img_idle.get_rect()

        self.image = self.img_idle

    def update(self, *event):
        self.rect.center = 640, 550
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.img_hovered
            if event[0].type == pygame.MOUSEBUTTONDOWN:
                set_game_stage('test')
        else:
            self.image = self.img_idle

        screen.blit(self.image, self.rect)


class Shit(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.img = load_image('lulza.jpg')

    def update(self, *event):
        screen.blit(self.img, (0, 0))

target_sprite_group = pygame.sprite.Group()
set_game_stage('menu')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
        target_sprite_group.update(event)
    pygame.display.flip()
    clock.tick(60)