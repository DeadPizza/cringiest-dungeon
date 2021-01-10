from stages.pg_utils import load_image, load_audio
import pygame
import json
import random

setGameStage = None
def makeStageFunc(func):
    global setGameStage
    setGameStage = func

def music_iter(iteration):
    if iteration < 3:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resources/audio/forest_theme.mp3')
        pygame.mixer.music.play(-1)
    elif 3 <= iteration < 6:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resources/audio/mm_music.mp3')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resources/audio/forest_theme.mp3')
        pygame.mixer.music.play(-1)

last_was = 'niggers'
def level_iter(iteration):
    global last_was
    now = ''
    if iteration == -1:
        return 'niggers'
    if iteration < 3:
        now = 'backs/map_RoyalForest.png'
    elif 3 <= iteration < 6:
        now = 'backs/map_AbandonedCastle.png'
    else:
        now = 'backs/testmap.png'

    if now != last_was:
        music_iter(iteration)

    return now
last_was = level_iter(-1)

class Skill:
    def __init__(self, num, name):
        f = open('resources/setups/skills_setup.json', encoding='UTF-8')
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
        sound = load_audio('skill_effect.mp3')
        sound.play()
        target.HP -= self.damage
        if target.HP < 0: target.HP = 0
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
        if trg.HP < 0: trg.HP = 0

class Inventory:
    def __init__(self, sprite):
        self.image = load_image(sprite)

class BattleController:
    def __init__(self, screen, controller):
        self.screen = screen
        self.controller = controller
        self.heroes = controller.heroes
        self.enemies_alive = 4
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
            if len(self.effectsToPerform) == 0: return
            for target, damage in self.effectsToPerform.pop(0):
                target.HP -= damage
                if target.HP < 0: target.HP = 0
        for c_enemy in self.enemies.copy():
            if c_enemy.HP == 0:
                for index in range(len(self.enemies)):
                    if self.enemies[index] == c_enemy:
                        del self.enemies[index]
                        break
                self.enemies_alive -= 1
                if self.enemies_alive == 0:
                    self.controller.destroyBattle()

    def performEnemyAction(self):
        for c_enemy in self.enemies:
            c_enemy.turn(self.heroes)

    def getCurrentHero(self):
        return self.heroes[self.queue_index]

    def renderBattle(self):
        if self.current_skill is not None:
            x, y = self.current_skill.icon_rect.topleft
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect((x, y), (64, 64)), 5)

class OnMapThing:
    def __init__(self, x, type_):
        self.type_ = type_
        self.x = x
        if self.type_ == 1:
            self.img = None
        elif self.type_ == 2:
            self.img = load_image('enemy.png')
    
    def trigger(self, controller):
        if self.type_ == 1:
            sound = load_audio('battle_start.mp3')
            sound.play()
            controller.makeBattle()
        else:
            print('потом добавлю')

class DungeonController:
    def __init__(self, screen, iteration, heroes_indexes):
        self.screen = screen
        self.iteration = iteration

        self.heroes = load_heroes(heroes_indexes)
        self.heroes_len = 4
        #self.enemies = [Enemy(1), Enemy(2), Enemy(3), Enemy(4)]
        self.hero_current = None
        self.hero_UI_font = pygame.font.SysFont('Arial', 20)

        self.map_image = load_image(level_iter(iteration))
        self.map_image_rect = self.map_image.get_rect()
        self.map_dx = 0
        self.map_moving = False

        self.inventory = Inventory('backs/inventory_test.png')

        self.BATTLE = False

        self.cursor_img = load_image('arrow.png')
        self.cursor_rect = self.cursor_img.get_rect()

        self.cursor_rect.topleft = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_img, self.cursor_rect)

        self.FADEOUT_FLAG = False
        self.FADEIN_FLAG = True
        self.ALPHA_FADE = 255
        self.alphaSurf = pygame.Surface((1280, 720))
        self.alphaSurf.fill((0, 0, 0))
        self.alphaSurf.set_alpha(self.ALPHA_FADE)
        self.otherObjects = []
        self.makeContent()

    def makeContent(self):
        for i in range(5):
            res = random.choice((0, 0, 1, 2))
            if i * res == 0: continue
            self.otherObjects.append(OnMapThing(-215 + 430 * (i + 1), res))
        print(self.otherObjects)

    def fadeout(self):
        self.renderUI()
        self.renderHeroes()
        self.ALPHA_FADE += 3
        if self.ALPHA_FADE >= 255:
            self.FADEOUT_FLAG = False
            self.__init__(self.screen, self.iteration + 1)
        self.alphaSurf.set_alpha(self.ALPHA_FADE)
        self.screen.blit(self.alphaSurf, (0, 0))

    def fadein(self):
        self.renderUI()
        self.renderHeroes()
        self.ALPHA_FADE -= 3
        if self.ALPHA_FADE <=3:
            self.FADEIN_FLAG = False
        self.alphaSurf.set_alpha(self.ALPHA_FADE)
        self.screen.blit(self.alphaSurf, (0, 0))

    def update(self):
        if self.FADEOUT_FLAG:
            self.fadeout()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            return
        
        if self.FADEIN_FLAG:
            self.fadein()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            return
            
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.onClickDown(mpos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.onClickUp()
            elif event.type == pygame.MOUSEMOTION:
                self.handleMouseMotion(event, mpos)
            #elif event.type == pygame.KEYDOWN:
            #    self.makeBattle()

        if self.map_moving:
            self.map_dx -= 1
            self.map_dx -= 4 * (1 - 2 * (mpos[0] < 640))
            if self.map_dx > 0:
                self.map_dx = 0
            elif self.map_dx < -1650:
                self.map_dx = -1650
                self.ALPHA_FADE = 0
                self.FADEOUT_FLAG = True
                return

            for obj in self.otherObjects:
                if obj.x - 2 <= -self.map_dx + 400 <= obj.x + 2:
                    obj.trigger(self)
                #self.__init__(self.screen, self.iteration + 1)


        self.renderUI()
        self.renderHeroes()
        if self.BATTLE:
            self.battle_cont.renderEnemies()
            self.battle_cont.renderBattle()
        self.renderCursor()

    def handleMouseMotion(self, event, mpos):
        self.cursor_rect.topleft = mpos

    def makeBattle(self):
        if self.BATTLE:
            return
        self.battle_cont = BattleController(self.screen, self)
        self.BATTLE = True
        self.map_moving = False
        self.hero_current = self.battle_cont.getCurrentHero()

    def destroyBattle(self):
        if not self.BATTLE:
            return
        del self.battle_cont
        self.BATTLE = False
        self.hero_current = None

    def renderUI(self):
        self.screen.blit(self.map_image, (self.map_dx, 0))
        for obj in self.otherObjects:
            if obj.type_ == 1: continue
            self.screen.blit(obj.img, (obj.x + self.map_dx, 100))
        self.screen.blit(self.inventory.image, (0, 420))

    def renderCursor(self):
        if pygame.mouse.get_focused():
            self.screen.blit(self.cursor_img, self.cursor_rect)

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
            try:
                self.hero_current = self.battle_cont.getCurrentHero()
            except AttributeError:
                self.hero_current = None
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
        for index in range(self.heroes_len):
            if self.heroes[index].image_rect.collidepoint(mpos):
                return index + 1
        return 0

    def checkEnemies(self, mpos):
        for index in range(self.battle_cont.enemies_alive):
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
