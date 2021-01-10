import pygame
from stages.pg_utils import load_image, load_audio

setGameStage = None
def makeStageFunc(func):
    global setGameStage
    setGameStage = func

class MenuController:
    def __init__(self, screen):
        self.screen = screen

        self.background = load_image('backs/bg_main_menu.png')
        pygame.mixer.music.load('resources/audio/mm_music.ogg')
        pygame.mixer.music.play(-1)

        self.start_img_idle = load_image('button_main_menu_start_idle.png')
        self.start_img_hovered = load_image('button_main_menu_start_hovered.png')
        self.start_rect = self.start_img_idle.get_rect()
        self.start_rect.center = 640, 550
        self.start_image = self.start_img_idle

        pygame.mouse.set_visible(False)
        self.cursor_img = load_image('arrow.png')
        self.cursor_rect = self.cursor_img.get_rect()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEMOTION:
                self.handleMouse(event, pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(event, pygame.mouse.get_pos())

        self.renderUI()

    def handleMouse(self, event, mpos):
        self.cursor_rect.topleft = mpos
        if self.start_rect.collidepoint(mpos):
            self.start_image = self.start_img_hovered
        else:
            self.start_image = self.start_img_idle

    def handleClick(self, event, mpos):
        if self.start_rect.collidepoint(mpos):
            pygame.mixer.music.stop()
            setGameStage(1)
    
    def renderUI(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.start_image, self.start_rect)
        if pygame.mouse.get_focused():
            self.screen.blit(self.cursor_img, self.cursor_rect)