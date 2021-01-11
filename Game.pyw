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
setGameStage(0)
while True:
    target.update()
    pygame.display.flip()
    clock.tick(FPS)