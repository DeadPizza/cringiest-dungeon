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
        self.ass = PygameList(screen)

    def update(self, *args, **kwargs):
        self.screen.blit(self.background, (0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.ass.update(event)
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


class PyListItem:
    def __init__(self, pos, num):
        self.x, self.y = pos
        self.num = num
        self.tgl = False
        self.img = load_image('UI/cringlet_select_char.png')
        self.img2 = load_image('UI/cringlet_select_char_selected.png')
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def toggle(self):
        self.tgl = not self.tgl
        if self.tgl:
            self.image = self.img2
        else:
            self.image = self.img

    def update(self, screen, dy):
        self.rect.topleft = self.x, self.y + dy
        screen.blit(self.image, (self.x, self.y + dy))
class PygameList:
    def __init__(self, screen):
        self.screen = screen
        self.li = [PyListItem((1040, 10 + 96 * i), i) for i in range(10)]
        self.selected = []
        self.dy = 0

        self.back = load_image('UI/cringlet_select_back.png')
        self.overlay= load_image('UI/cringlet_select_overlay.png')

    def update(self, event):
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.dy += 32
            elif event.button == 5:
                self.dy -= 32
            elif event.button == 1:
                mpos = pygame.mouse.get_pos()
                for i in self.li:
                    if i.rect.collidepoint(mpos):
                        i.toggle()
                        if i.tgl:
                            self.selected.append(i)
                            if len(self.selected) > 4:
                                elem = self.selected.pop(0)
                                elem.toggle()
                        else:
                            for j in range(len(self.selected.copy())):
                                if self.selected[j] == i:
                                    del self.selected[j]
                                    break
            elif event.button == 2:
                for i in range(len(self.selected.copy())):
                    self.selected[0].toggle()
                    del self.selected[0]

                                    

        self.screen.blit(self.back, (1030, 0))
        for i in self.li:
            i.update(self.screen, self.dy)
        self.screen.blit(self.overlay, (1030, 0))


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