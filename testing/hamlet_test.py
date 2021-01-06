import pygame
from settings import *
from test import load_image

pygame.init()
clock = pygame.time.Clock()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
background = load_image('cringlet/background.png')

class Building(pygame.sprite.Sprite):
    def __init__(self, group, screen, texture, coords):
        super().__init__(group)
        self.screen = screen
        self.img = load_image(f'cringlet/{texture}')
        self.rect = self.img.get_rect()
        self.rect.topleft = coords
    
    def update(self, *event):
        self.screen.blit(self.img, self.rect)

trg = pygame.sprite.Group()
Sobor = Building(trg, screen, 'sobor.png', (482, 250))
Graves = Building(trg, screen, 'graves.png', (500, 400))
Guild = Building(trg, screen, 'guild.png', (720, 320))
Durka = Building(trg, screen, 'durka.png', (280, 300))
Kuznya = Building(trg, screen, 'kuznya.png', (800, 400))
Traktir = Building(trg, screen, 'traktir.png', (150, 450))
Dilijans = Building(trg, screen, 'dilijans.png', (120, 600))

font = pygame.font.SysFont("Arial", 18) 
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text

while True:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
    trg.update()
    screen.blit(update_fps(), (5, 5))
    pygame.display.flip()
    clock.tick()