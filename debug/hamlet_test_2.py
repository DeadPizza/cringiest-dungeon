import pygame
from test import load_image, load_audio

class Building:
    def __init__(self, image, coords):
        self.image = load_image(f'cringlet/{image}')
        self.x, self.y = coords
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

class CringletController:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_image('cringlet/background.png')
        self.goToDungeon = load_image('UI/cringlet_start_dungeon.png')
        self.goToDungeon_rect = self.goToDungeon.get_rect()
        self.goToDungeon_rect.topleft = 515, 650 
        self.buildings = [
            Building('sobor.png', (482, 250)),
            Building('graves.png', (500, 400)),
            Building('guild.png', (720, 320)),
            Building('durka.png', (280, 300)),
            Building('kuznya.png', (810, 490)),
            Building('traktir.png', (150, 450)),
            Building('dilijans.png', (120, 600))
        ]
        self.choose_list = PygameList(self.screen)

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                self.handleMouse(event, mpos)
                self.choose_list.handleMouse(event, mpos)

        self.renderBack()
        self.renderBuildings()
        self.renderUI()

    def handleMouse(self, event, mpos):
        for ind in range(len(self.buildings) - 1, -1, -1):
            if self.buildings[ind].rect.collidepoint(mpos):
                print('got it')
                return

        if self.goToDungeon_rect.collidepoint(mpos):
            setGameStage(2)
            return

    def renderUI(self):
        self.choose_list.renderList()
        self.screen.blit(self.goToDungeon, self.goToDungeon_rect)
    def renderBuildings(self):
        for c_building in self.buildings:
            self.screen.blit(c_building.image, c_building.rect)
    def renderBack(self):
        self.screen.blit(self.background, (0, 0))

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
        cur_y = self.y + dy
        self.rect.topleft = self.x, cur_y
        if cur_y > 720 or cur_y < 0:
            return
        screen.blit(self.image, (self.x, cur_y))

class PygameList:
    def __init__(self, screen):
        self.screen = screen
        self.li = [PyListItem((1040, 10 + 96 * i), i) for i in range(10)]
        self.selected = []
        self.dy = 0

        self.back = load_image('UI/cringlet_select_back.png')
        self.overlay= load_image('UI/cringlet_select_overlay.png')

    def handleMouse(self, event, mpos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.dy += 32
            elif event.button == 5:
                self.dy -= 32
            elif event.button == 1:
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

    def renderList(self):
        self.screen.blit(self.back, (1030, 0))
        for i in self.li:
            i.update(self.screen, self.dy)
        self.screen.blit(self.overlay, (1030, 0))

if __name__ == '__main__':
    from settings import *
    pygame.init()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    trg = CringletController(screen)

    font = pygame.font.SysFont("Arial", 18)
    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text
    
    while True:
        #screen.fill((0, 0, 0))
        trg.update()
        screen.blit(update_fps(), (5, 5))
        pygame.display.flip()
        clock.tick()