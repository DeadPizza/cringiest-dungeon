import pygame
import stages.menu as menu
import stages.cringlet as cringlet
import stages.dungeon as dungeon
from stages.settings import *
from threading import Thread
from debug.console_commands import cmd_dict

class Console(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.parseCMD(input())

    def parseCMD(self, cmd):
        try:
            cmd = cmd.split()
            command = cmd[0]
            args = cmd[1:]
            cmd_dict[command](target, *args)
        except AttributeError as msg:
            print(f'ERROR: {msg}.\nIs this room right?')
        except IndexError:
            print(f'ERROR has occured while parsing command')
        except:
            print('unknown error')

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

font = pygame.font.SysFont("Arial", 18)
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

target = None
setGameStage(0)
DebugConsole = Console()
DebugConsole.start()
while True:
    target.update()
    screen.blit(update_fps(), (5, 5))
    pygame.display.flip()
    clock.tick(FPS)