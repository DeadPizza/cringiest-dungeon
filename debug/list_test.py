import pygame
from settings import *
from test import load_image

pygame.init()
clock = pygame.time.Clock()
size = 1280, 720
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("Arial", 18) 
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text


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

    def update(self):
        events = pygame.event.get()
        for event in events:
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

ass = PygameList(screen)
while True:
    screen.fill((0,0,0))
    ass.update()
    screen.blit(update_fps(), (5, 5))
    pygame.display.flip()
    clock.tick(FPS)