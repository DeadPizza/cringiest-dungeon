from test import load_image
import pygame
import json
import random

class Skill:
    def __init__(self, num, name):
        f = open('D:/cringiest dungeon/resources/setups/skills_setup.json', encoding='UTF-8')
        data = json.load(f)[name]
        self.num = num
        self.title = data['title']
        self.icon = load_image(data['icon'])
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.topleft = (310 + 81 * (num - 1), 455)
        self.damage = data['damage']
        self.effect = data['effect']
        if self.effect:
            self.turn_effect = data['effect_list']

        f.close()
        del data

    def work(self, target, toPerform):
        target.HP -= self.damage
        for i in range(self.effect):
            try:
                toPerform[i].append((target, self.turn_effect[i]['damage']))
            except IndexError:
                toPerform.append([])
                toPerform[i].append((target, self.turn_effect[i]['damage']))

class Hero:
    def __init__(self, number, data):
        self.x = 10 + 120 * (number - 1)
        self.number = number

        self.image = load_image(data['texture'])
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, 150)
        self.ico = load_image(data['icon'])

        self.HP, self.MAX_HP = 100, 100
        self.STRESS = 10
        self.name = data['name']
        self.skills = [Skill(num + 1, sk) for num, sk in enumerate(data['skills'])]

class Enemy:
    def __init__(self, number, *data):
        self.x = 1170 - 120 * (number - 1)

        self.image = load_image('enemy.png')
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (self.x, 150)
        self.HP, self.MAX_HP = 100, 100
        self.skills = [
            Skill(1, "warrior.attack"),
            Skill(2, "warrior.attack"),
            Skill(3, "warrior.attack"),
            Skill(4, "warrior.attack")
        ]
    def turn(self, heroes):
        sk = random.choice(self.skills)
        trg = random.choice(heroes)

        trg.HP -= sk.damage

class Inventory:
    def __init__(self, sprite):
        self.image = load_image(sprite)

class BattleController:
    def __init__(self, screen, pls):
        self.screen = screen
        self.heroes = pls
        self.enemies = [Enemy(1), Enemy(2), Enemy(3), Enemy(4)]
        self.player_target = None
        self.current_skill = None

        self.queue_index = 0
        self.turn = 0
        self.effectsToPerform = []

    def renderEnemies(self):
        for c_enemy in self.enemies:
            self.screen.blit(c_enemy.image, (c_enemy.x, 150))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((c_enemy.x, 375), (100, 10)))
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect((c_enemy.x + 1, 376), (c_enemy.HP / c_enemy.MAX_HP * 100 - 2, 8)))

    def performAction(self):
        self.current_skill.work(self.player_target, self.effectsToPerform)
        self.current_skill = None
        self.player_target = None
        self.queue_index += 1
        if self.queue_index > 3:
            self.queue_index = 0
            self.performEnemyAction()
            self.turn += 1
            for target, damage in self.effectsToPerform.pop(0):
                target.HP -= damage

    def performEnemyAction(self):
        for c_enemy in self.enemies:
            c_enemy.turn(self.heroes)

    def getCurrentHero(self):
        return self.heroes[self.queue_index]

    def renderBattle(self):
        if self.current_skill is not None:
            x, y = self.current_skill.icon_rect.topleft
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect((x, y), (64, 64)), 5)

class DungeonController:
    def __init__(self, screen):
        self.screen = screen

        self.heroes = load_heroes((0, 1, 2, 3))
        #self.enemies = [Enemy(1), Enemy(2), Enemy(3), Enemy(4)]
        self.hero_current = None
        self.hero_UI_font = pygame.font.SysFont('Arial', 20)

        self.map_image = load_image('backs/testmap.png')
        self.map_image_rect = self.map_image.get_rect()
        self.map_dx = 0
        self.map_moving = False

        self.inventory = Inventory('backs/inventory_test.png')

        self.BATTLE = False

    def update(self):
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.onClickDown(mpos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.onClickUp()
            elif event.type == pygame.KEYDOWN:
                self.makeBattle()

        if self.map_moving:
            self.map_dx -= 1
            self.map_dx -= 3 * (1 - 2 * (mpos[0] < 640))
            if self.map_dx > 0:
                self.map_dx = 0
            elif self.map_dx < -1650:
                self.map_dx = -1650


        self.renderUI()
        self.renderHeroes()
        if self.BATTLE:
            self.battle_cont.renderEnemies()
            self.battle_cont.renderBattle()

    def makeBattle(self):
        if self.BATTLE:
            return
        self.battle_cont = BattleController(self.screen, self.heroes)
        self.BATTLE = True
        self.map_moving = False
        self.hero_current = self.battle_cont.getCurrentHero()

    def renderUI(self):
        self.screen.blit(self.map_image, (self.map_dx, 0))
        self.screen.blit(self.inventory.image, (0, 420))

    def renderHeroes(self):
        for hero in self.heroes:
            self.screen.blit(hero.image, (hero.x, 150))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((hero.x, 375), (100, 10)))
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect((hero.x + 1, 376), (hero.HP / hero.MAX_HP * 100 - 2, 8)))
        if self.hero_current is not None:
            textsurface = self.hero_UI_font.render(str(self.hero_current.HP) + '/' + str(self.hero_current.MAX_HP), False, (255, 0, 0))
            self.screen.blit(textsurface, (115, 568))
            textsurface = self.hero_UI_font.render(str(self.hero_current.STRESS) + '/200', False, (255, 255, 255))
            self.screen.blit(textsurface, (115, 612))
            textsurface = self.hero_UI_font.render(self.hero_current.name, False, (255, 255, 255))
            self.screen.blit(textsurface, (183, 453))
            self.screen.blit(self.hero_current.ico, (113, 454))

            for index in range(4):
                self.screen.blit(self.hero_current.skills[index].icon, (310 + 81 * index, 455))

            x, y = self.hero_current.image_rect.topleft
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect((x, y), (100, 220)), 5)

    def onClickDown(self, mpos):
        if self.BATTLE and self.battle_cont.current_skill is not None:
            target = self.checkEnemies(mpos)
            if not target:
                self.battle_cont.current_skill = None
                return
            self.battle_cont.player_target = self.battle_cont.enemies[target - 1]
            #print(f'{target} ща сдохнет')
            self.battle_cont.performAction()
            self.hero_current = self.battle_cont.getCurrentHero()
            return

        if self.hero_current is not None:
            skill = self.checkSkill(mpos)
            if skill and self.BATTLE:
                self.battle_cont.current_skill = self.hero_current.skills[skill - 1]
                #print(self.hero_current.skills[skill - 1].title)
                return

        if self.BATTLE:
            return

        index = self.checkHeroes(mpos)
        #print(mpos)
        if index:
            self.hero_current = self.heroes[index - 1]
        elif not self.BATTLE:
            self.hero_current = None
            if self.map_image_rect.collidepoint(mpos):
                self.map_moving = True

    def onClickUp(self):
        self.map_moving = False

        
    def checkHeroes(self, mpos):
        for index in range(4):
            if self.heroes[index].image_rect.collidepoint(mpos):
                return index + 1
        return 0

    def checkEnemies(self, mpos):
        for index in range(4):
            if self.battle_cont.enemies[index].image_rect.collidepoint(mpos):
                return index + 1
        return 0

    def checkSkill(self, mpos):
        for index in range(4):
            if self.hero_current.skills[index].icon_rect.collidepoint(mpos):
                return index + 1
        return 0


def load_heroes(indexes):
    f = open('save/heroes.json', encoding='UTF-8') 
    saved_data = json.load(f)
    heroes = []
    for j, i in enumerate(indexes):
        heroes.append(Hero(j + 1, saved_data[i]))
    f.close()
    return heroes


if __name__ == '__main__':
    from settings import *
    pygame.init()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    trg = DungeonController(screen)

    font = pygame.font.SysFont("Arial", 18)
    def update_fps():
        fps = str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text
    
    while True:
        screen.fill((0, 0, 0))
        trg.update()
        screen.blit(update_fps(), (5, 5))
        pygame.display.flip()
        clock.tick()