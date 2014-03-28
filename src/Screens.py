'''
Created on Jan 4, 2012

@author: Wolmir Nemitz
'''
import pygame, GameWorld, Physics, sys, random
from pygame.locals import K_PAUSE
from pygame.locals import K_RETURN
from pygame.locals import K_UP
from pygame.locals import K_DOWN

class Screen:
    def __init__(self, size, manager):
        self.counter = 0.0
        self.inps = []
        self.size = size
        self.manager = manager
        
    def update(self, time):
        self.counter = time
    
    def control_input(self, inp):
        try:
            self.inps.index(inp)
        except ValueError:
            self.inps.append(inp)
    
    def control_release(self, inp):
        try:
            self.inps.remove(inp)
        except ValueError:
            print ""



class ScreenManager:
    
    def __init__(self):
        self.currentScreen = None
    
    def changeScreen(self, screen):
        self.currentScreen = screen
        

class GameScreen(Screen):
    
    def __init__(self, size, manager):
        Screen.__init__(self, size, manager)
        self.paused_image = pygame.image.load('paused.png')
        self.playerShipImage = pygame.image.load('PlayerShip.png')
        self.enemyShipImage = pygame.image.load('enemyShip.png')
        self.world = GameWorld.World(self.size)
        self.shotImg = pygame.image.load('shotImg.png')
        self.killImgs = []
        self.explosionImg = pygame.image.load('explode_1.png')
        for z in range(0, 4):
            for w in range(0, 4):
                self.killImgs.append(pygame.Surface((64, 64)))
                self.killImgs[(z * 4) + w].blit(self.explosionImg, pygame.Rect((0, 0), (64, 64)), pygame.Rect((w * 64, z * 64), (64, 64)))
        self.playerShip = GameWorld.PlayerShip(self.world, self.playerShipImage, self.killImgs)
        self.playerShip.shotImg = self.shotImg
        self.playerShip.pData.position = Physics.Vector2D(300, 600)
        self.world.addObject(self.playerShip)
        self.pause = False
        self.pauseHit = False
        self.group = []
        for i in range(0, 1):
            self.group.append(GameWorld.EnemyShip(self.world, self.enemyShipImage, self.group, self.killImgs))
            self.group[i].shotImg = self.shotImg
            self.group[i].pData.position = Physics.Vector2D(300, 400)
            self.world.addObject(self.group[i])
            
    def control_release(self, inp):
        Screen.control_release(self, inp)
        self.playerShip.controlPanel.control_release(inp)
        if inp == K_PAUSE:
            self.pauseHit = True
    
    def update(self, time):
        Screen.update(self, time)
        for e in self.inps:
            if (e == K_PAUSE) and self.pauseHit:
                self.pause = not self.pause
                self.pauseHit = False
            self.playerShip.controlPanel.control_input(e)
            #self.control_release(e)
        if self.pause:
            return
        self.world.update(self.counter)
        tmpScore = self.playerShip.score
        self.playerShip.score += self.world.clearDeadPeople(self.group)
        if not tmpScore == self.playerShip.score:
            self.playerShip.score += 13
            for i in range(0, 2):
                if len(self.group) > 4:
                    break
                x = random.randint(50, self.size[0] - 50)
                y = random.randint(50, self.size[1] - 50)
                self.group.append(GameWorld.EnemyShip(self.world, self.enemyShipImage, self.group, self.killImgs))
                self.group[len(self.group) - 1].shotImg = self.shotImg
                self.group[len(self.group) - 1].pData.position = Physics.Vector2D(x, y)
                self.world.addObject(self.group[len(self.group) - 1])
        if not self.playerShip.lifeStatus:
            self.manager.changeScreen(ScoreScreen(self.size, self.manager, self.playerShip.score))
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.world.draw(screen)
        if self.pause:
            rect = self.paused_image.get_rect()
            rect.center = (self.size[0] / 2, self.size[1] / 2)
            screen.blit(self.paused_image, rect)


class StartScreen(Screen):
    def __init__(self, size, manager):
        Screen.__init__(self, size, manager)
        self.startImage = pygame.image.load('start_game.png')
        self.startImageSelected = pygame.image.load('start_game_selected.png')
        self.quitImage = pygame.image.load('quit.png')
        self.quitImageSelected = pygame.image.load('quit_selected.png')
        self.titleImage = pygame.image.load('title.png')
        self.start = True
        self.quit = False
    
    def update(self, time):
        Screen.update(self, time)
        for e in self.inps:
            if e == K_RETURN:
                if self.start:
                    self.manager.currentScreen = GameScreen(self.size, self.manager)
                elif self.quit:
                    pygame.quit()
                    sys.exit()
            if e == K_UP or e == K_DOWN:
                self.start = not self.start
                self.quit = not self.quit
                self.control_release(e)
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        title_rect = self.titleImage.get_rect()
        title_rect.center = (190, 150)
        screen.blit(self.titleImage, title_rect)
        if not self.start:
            start_rect = self.startImage.get_rect()
            start_rect.center = (self.size[0] / 2, (self.size[1] / 2) - 25)
            screen.blit(self.startImage, start_rect)
        else:
            start_sel_rect = self.startImageSelected.get_rect()
            x = self.size[0] / 2 + 50
            y = self.size[1] / 2 - 25
            start_sel_rect.center = (x, y)
            screen.blit(self.startImageSelected, start_sel_rect)
        if not self.quit:
            quit_rect = self.quitImage.get_rect()
            quit_rect.center = (self.size[0] / 2, (self.size[1] / 2) + 25)
            screen.blit(self.quitImage, quit_rect)
        else:
            quit_sel_rect = self.quitImageSelected.get_rect()
            quit_sel_rect.center = ((self.size[0] / 2) + 50, (self.size[1] / 2) + 25)
            screen.blit(self.quitImageSelected, quit_sel_rect)


class ScoreScreen(Screen):
    def __init__(self, size, manager, score):
        Screen.__init__(self, size, manager)
        self.score = score
        self.scoreImg = pygame.image.load('score.png')
        self.numbers = []
        self.numbers.append(pygame.image.load('zero.png'))
        self.numbers.append(pygame.image.load('one.png'))
        self.numbers.append(pygame.image.load('two.png'))
        self.numbers.append(pygame.image.load('three.png'))
        self.numbers.append(pygame.image.load('four.png'))
        self.numbers.append(pygame.image.load('five.png'))
        self.numbers.append(pygame.image.load('six.png'))
        self.numbers.append(pygame.image.load('seven.png'))
        self.numbers.append(pygame.image.load('eight.png'))
        self.numbers.append(pygame.image.load('nine.png'))
    
    def update(self, time):
        Screen.update(self, time)
        for e in self.inps:
            if e == K_RETURN:
                self.manager.changeScreen(StartScreen(self.size, self.manager))
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        score_rect = self.scoreImg.get_rect()
        score_rect.center = ((self.size[0] / 2) - 100, self.size[1] / 2)
        screen.blit(self.scoreImg, score_rect)
        score_str = str(self.score)
        for i in range(0, len(score_str)):
            tmp_rect = self.numbers[int(score_str[i])].get_rect()
            tmp_rect.center = ((self.size[0] / 2) + (i * 40), self.size[1] / 2)
            screen.blit(self.numbers[int(score_str[i])], tmp_rect)


class MovementTestScreen(Screen):
    def __init__(self, size, manager):
        Screen.__init__(self, size, manager)
        self.playerShipImage = pygame.image.load('PlayerShip.png')
        self.world = GameWorld.World(self.size)
        self.shotImg = pygame.image.load('shotImg.png')
        self.killImgs = []
        self.explosionImg = pygame.image.load('explode_1.png')
        for z in range(0, 4):
            for w in range(0, 4):
                self.killImgs.append(pygame.Surface((64, 64)))
                self.killImgs[(z * 4) + w].blit(self.explosionImg, pygame.Rect((0, 0), (64, 64)), pygame.Rect((w * 64, z * 64), (64, 64)))
        self.playerShip = GameWorld.PlayerShip(self.world, self.playerShipImage, self.killImgs)
        self.playerShip.shotImg = self.shotImg
        self.playerShip.pData.position = Physics.Vector2D(300, 600)
        self.world.addObject(self.playerShip)
        self.lastPosition = (300, 600)
    
    
    def update(self, time):
        Screen.update(self, time)
        for e in self.inps:
            self.playerShip.controlPanel.control_input(e)
        self.world.update(self.counter)
    
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.aaline(screen, (0, 0, 150), (self.lastPosition[0], self.size[1]), (self.lastPosition[0], 0))
        pygame.draw.aaline(screen, (0, 0, 150), (0, self.lastPosition[1]), (self.size[0], self.lastPosition[1]))
        pygame.draw.aaline(screen, (150, 0, 0), (self.playerShip.pData.position.x, self.size[1]), (self.playerShip.pData.position.x, 0))
        pygame.draw.aaline(screen, (150, 0, 0), (0, self.playerShip.pData.position.y), (self.size[1], self.playerShip.pData.position.y))
        self.world.draw(screen)
        self.lastPosition = (self.playerShip.pData.position.x, self.playerShip.pData.position.y)



class CollisionTestScreen(Screen):
    def __init__(self, size, manager):
        Screen.__init__(self, size, manager)
        self.enemyShipImage = pygame.image.load('enemyShip.png')
        self.world = GameWorld.World(self.size)
        self.shotImg = pygame.image.load('shotImg.png')
        self.killImgs = []
        self.explosionImg = pygame.image.load('explode_1.png')
        self.group = []
        for z in range(0, 4):
            for w in range(0, 4):
                self.killImgs.append(pygame.Surface((64, 64)))
                self.killImgs[(z * 4) + w].blit(self.explosionImg, pygame.Rect((0, 0), (64, 64)), pygame.Rect((w * 64, z * 64), (64, 64)))
        for i in range(0, 2):
            self.group.append(GameWorld.EnemyShip(self.world, self.enemyShipImage, self.group, self.killImgs))
            self.group[i].shotImg = self.shotImg
            self.group[i].pData.position = Physics.Vector2D(20 * i + 100, 20 * i + 100)
            self.world.addObject(self.group[i])
        self.group[0].goingToDie = True
    
    
    def update(self, time):
        Screen.update(self, time)
        self.world.update(self.counter)
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        for ship in self.group:
            pos = ship.pData.position
            rct = ship.pData.colRect
            pygame.draw.rect(screen, (150, 0, 0), pygame.Rect((pos.x - rct[0] / 2, pos.y - rct[1] / 2), (rct[0], rct[1])))
        self.world.draw(screen)



class ScoreTestScreen(Screen):   
    def __init__(self, size, manager):
        Screen.__init__(self, size, manager)
        self.playerShipImage = pygame.image.load('PlayerShip.png')
        self.enemyShipImage = pygame.image.load('enemyShip.png')
        self.world = GameWorld.World(self.size)
        self.shotImg = pygame.image.load('shotImg.png')
        self.killImgs = []
        self.explosionImg = pygame.image.load('explode_1.png')
        for z in range(0, 4):
            for w in range(0, 4):
                self.killImgs.append(pygame.Surface((64, 64)))
                self.killImgs[(z * 4) + w].blit(self.explosionImg, pygame.Rect((0, 0), (64, 64)), pygame.Rect((w * 64, z * 64), (64, 64)))
        self.playerShip = GameWorld.PlayerShip(self.world, self.playerShipImage, self.killImgs)
        self.playerShip.shotImg = self.shotImg
        self.playerShip.pData.position = Physics.Vector2D(300, 600)
        self.world.addObject(self.playerShip)
        self.pause = False
        self.pauseHit = False
        self.group = []
        for i in range(0, 1):
            self.group.append(GameWorld.EnemyShip(self.world, self.enemyShipImage, self.group, self.killImgs))
            self.group[i].shotImg = self.shotImg
            self.group[i].pData.position = Physics.Vector2D(300, 400)
            self.world.addObject(self.group[i])
            self.group[i].ai.shoot = True
            
    def control_release(self, inp):
        Screen.control_release(self, inp)
        self.playerShip.controlPanel.control_release(inp)
        '''if inp == K_PAUSE:
            self.pauseHit = True'''
    
    def update(self, time):
        Screen.update(self, time)
        for e in self.inps:
            '''if (e == K_PAUSE) and self.pauseHit:
                self.pause = not self.pause
                self.pauseHit = False'''
            self.playerShip.controlPanel.control_input(e)
            #self.control_release(e)
        '''if self.pause:
            return'''
        self.world.update(self.counter)
        tmpScore = self.playerShip.score
        self.playerShip.score += self.world.clearDeadPeople(self.group)
        if not tmpScore == self.playerShip.score:
            self.playerShip.score += 13
        if not (self.playerShip.lifeStatus and (len(self.group) > 0)):
            self.manager.changeScreen(ScoreScreen(self.size, self.manager, self.playerShip.score))
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.world.draw(screen)
        '''if self.pause:
            rect = self.paused_image.get_rect()
            rect.center = (self.size[0] / 2, self.size[1] / 2)
            screen.blit(self.paused_image, rect)'''
