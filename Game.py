import pygame
import stages.menu as menu
import stages.cringlet as cringlet
import stages.dungeon as dungeon
from stages.settings import *


def setGameStage(stage, *args):
    global target
    global screen
    if stage == 0:
        target = menu.MenuController(screen)
    elif stage == 1:
        target = cringlet.CringletController(screen)
    elif stage == 2:
        target = dungeon.DungeonController(screen, 0, args[0])

menu.makeStageFunc(setGameStage)
cringlet.makeStageFunc(setGameStage)
dungeon.makeStageFunc(setGameStage)

pygame.init()
clock = pygame.time.Clock()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
target = None

font = pygame.font.SysFont("Arial", 18)
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

setGameStage(0)
while True:
    target.update()
    screen.blit(update_fps(), (5, 5))
    pygame.display.flip()
    clock.tick(FPS)