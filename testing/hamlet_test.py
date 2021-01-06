import pygame
from settings import *
from test import load_image

pygame.init()
clock = pygame.time.Clock()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

class Building(pygame.sprite.Sprite):
    def __init__(self, group, screen, texture, coords):
        super().__init__(group)
        self.screen = screen
        self.img = load_image(f'cringlet/{texture}')
        self.rect = self.img.get_rect()
        self.rect.topleft = coords
        self.test = texture
    
    def update(self):
        self.screen.blit(self.img, self.rect)

    def on_click(self):
        print(self.test)
        self.update()

class CringletGroup(pygame.sprite.Group):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.background = load_image('cringlet/background.png')

    def update(self, *args, **kwargs):
        self.screen.blit(self.background, (0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                to_click = []
                for sprite in self.sprites():
                    if sprite.rect.collidepoint(mpos):
                        to_click.append((sprite, sprite.rect.y))
                if to_click:
                    res = sorted(to_click, key=lambda x: -x[1])[0][0]
                    for sprite in self.sprites():
                        if sprite == res:
                            sprite.on_click()
                        else:
                            sprite.update()
                return

        for sprite in self.sprites():
            sprite.update()

def create_CRINGLET_SCENE(screen):
    trg = CringletGroup(screen)
    Sobor = Building(trg, screen, 'sobor.png', (482, 250))
    Graves = Building(trg, screen, 'graves.png', (500, 400))
    Guild = Building(trg, screen, 'guild.png', (720, 320))
    Durka = Building(trg, screen, 'durka.png', (280, 300))
    Kuznya = Building(trg, screen, 'kuznya.png', (810, 490))
    Traktir = Building(trg, screen, 'traktir.png', (150, 450))
    Dilijans = Building(trg, screen, 'dilijans.png', (120, 600))
    return trg

CRINGLET_SCENE = create_CRINGLET_SCENE(screen)

font = pygame.font.SysFont("Arial", 18) 
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text

while True:
    CRINGLET_SCENE.update()
    screen.blit(update_fps(), (5, 5))
    pygame.display.flip()
    clock.tick()