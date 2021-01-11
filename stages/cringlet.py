import pygame
from stages.pg_utils import load_image, load_audio
import json

setGameStage = None
def makeStageFunc(func):
    global setGameStage
    setGameStage = func

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

        self.cursor_img = load_image('arrow.png')
        self.cursor_rect = self.cursor_img.get_rect()

        self.cursor_rect.topleft = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, self.cursor_rect)

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                self.handleMouse(event, mpos)
                self.choose_list.handleMouse(event, mpos)
            elif event.type == pygame.MOUSEMOTION:
                self.handleMouseMotion(event, pygame.mouse.get_pos())

        self.renderBack()
        self.renderBuildings()
        self.renderUI()

    def handleMouseMotion(self, event, mpos):
        self.cursor_rect.topleft = mpos

    def handleMouse(self, event, mpos):
        for ind in range(len(self.buildings) - 1, -1, -1):
            if self.buildings[ind].rect.collidepoint(mpos):
                print('got it')
                return

        if self.goToDungeon_rect.collidepoint(mpos):
            #print('start dungeon')
            choosen = [i.num for i in self.choose_list.selected]
            if len(choosen) != 4:
                return
            setGameStage(2, choosen)
            return

    def renderUI(self):
        self.choose_list.renderList()
        self.screen.blit(self.goToDungeon, self.goToDungeon_rect)
        if pygame.mouse.get_focused():
            self.screen.blit(self.cursor_img, self.cursor_rect)
    def renderBuildings(self):
        for c_building in self.buildings:
            self.screen.blit(c_building.image, c_building.rect)
    def renderBack(self):
        self.screen.blit(self.background, (0, 0))

class PyListItem:
    def __init__(self, pos, num, data):
        self.x, self.y = pos
        self.num = num
        self.tgl = False
        self.hero_name = data['name']
        self.hero_UI_font = pygame.font.SysFont('Arial', 15)
        self.hero_icon = load_image(data['icon'])
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
        screen.blit(self.hero_icon, (self.x, cur_y))
        textsurface = self.hero_UI_font.render(self.hero_name, False, (255, 255, 255))
        screen.blit(textsurface, (self.x + 66, cur_y + 5))

class PygameList:
    def __init__(self, screen):
        self.screen = screen
        self.li = load_all_chars()
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


def load_all_chars():
    f = open('save/heroes.json', encoding='UTF-8') 
    saved_data = json.load(f)
    heroes = []
    for j, i in enumerate(saved_data):
        heroes.append(PyListItem((1040, 10 + 96 * j), j, i))
    f.close()
    return heroes