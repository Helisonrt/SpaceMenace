# -*- coding: utf-8 -*-
'''
Created on Nov 26, 2011

@author: Wolmir Nemitz
'''

import Physics
#import pygame
import random
from pygame.locals import K_UP
from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_SPACE

#--------------------------------------- World Definition ------------------------------
class World:
    '''
    Esta classe mantém todos os objetos do jogo.
    A cada loop ela é atualizada. Em cada atualização
    ela verifica as colisões e remove os objetos mortos.
    À ela também é delegada a tarefa de desenhar os objetos.
    '''
    def __init__(self, size):
        self.sm_objects = []
        self.size = size
    
    def addObject(self, sm_object):
        self.sm_objects.append(sm_object)
        sm_object.pData.dimension = self.size
        
    def update(self, time):
        for i in self.sm_objects:
            i.update(time)
            if i.lifeStatus:
                for j in self.sm_objects:
                    if i == j:
                        continue
                    if i.pData.collide(j.pData, time): #Se houve colisão entre dois objetos...
                        i.kill() #... mate os dois.
                        j.kill()
                    i.pData.lastCollision = time
            
    def resize(self, newSize):
        self.size = newSize
        for i in self.sm_objects:
            i.dimension = self.size
            
    def clearDeadPeople(self, group):
        counter = 0
        deadPeople = []
        for i in self.sm_objects:
            if not i.lifeStatus:
                deadPeople.append(i)
                if isinstance(i, EnemyShip): #Se o objeto morto for um inimigo, aumente os pontos.
                    counter += 1
                    group.remove(i)
        for a in deadPeople:
            self.sm_objects.remove(a)
        return counter
    
    def draw(self, screen):
        for i in self.sm_objects:
            i.draw(screen) # A tarefa de desenhar é delegada a cada objeto.

#---------------------------------------------------------------------------------------------------------

#----------------------------------------------------------- Object Definition ---------------------------
class Object:
    '''
    Classe para representar os objetos f�sicos do jogo.
    '''
    def __init__(self, world, img):
        self.img = img
        self.world = world
        self.lifeStatus = True
        self.pData = Physics.PhysicsData((0, 0), (100, 100))
    
    def update(self, time):
        self.pData.update(time)
        if self.pData.dead:
            self.lifeStatus = False
        
    def draw(self, screen):
        rect = self.img.get_rect()
        rect.center = (self.pData.position.x, self.pData.position.y)
        screen.blit(self.img, rect)
    
    def kill(self):
        self.lifeStatus = False

#-------------------------------------------------------------------------------------------------------

#------------------------------------------------------ Control Panel Definition -----------------------
CONTROLLER_UP      = K_UP
CONTROLLER_RIGHT   = K_RIGHT
CONTROLLER_DOWN    = K_DOWN
CONTROLLER_LEFT    = K_LEFT
CONTROLLER_TRIGGER = K_SPACE

class ShipControlPanel:
    '''
    Classe que serve para filtrar o ruído dos inputs do
    usuário. Quando uma tecla é apertada, o controle
    é inserido aqui. Quando a tecla é solta, o controle
    também é solto aqui. Um mesmo controle não pode
    ser inserido ou removido duas vezes, o que estabiliza
    um pouco o comportamento da nave.
    '''
    def __init__(self):
        self.active_controls = []
    
    def control_input(self, control):
        try:
            self.active_controls.index(control)
        except ValueError:
            self.active_controls.append(control)
            
    def control_release(self, control):
        try:
            self.active_controls.remove(control)
        except ValueError:
            print ""
#-------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------- Ship Definition ----------------------
class Ship(Object):
    '''
    Classe que representa todas as naves.
    '''
    def __init__(self, world, img, killImgs, shotImg=None):
        Object.__init__(self, world, img)
        self.shotImg = shotImg
        self.controlPanel = ShipControlPanel();
        self.pData.MAX_SPEED = 10;
        self.shotImg = None
        self.lastShot = 0.0
        self.shotFrequency = 0.4
        self.killImgs = killImgs
        self.goingToDie = False
        self.dieImg = 0
    
    '''
    O update da nave é feito antes do update do
    objeto, para que os controles sejam processados
    imediatamente.
    '''
    def update(self, time):
        if self.goingToDie:
            self.img = self.killImgs[self.dieImg]
            self.dieImg += 1
            if self.dieImg >= len(self.killImgs):
                Object.kill(self)
            return
        self.pData.velocity = Physics.Vector2D();
        
        for i in self.controlPanel.active_controls:
            if i == CONTROLLER_UP:
                self.pData.incVelocity(Physics.Vector2D(0, -1))
            elif i == CONTROLLER_DOWN:
                self.pData.incVelocity(Physics.Vector2D(0, 1))
            elif i == CONTROLLER_LEFT:
                self.pData.incVelocity(Physics.Vector2D(-1, 0))
            elif i == CONTROLLER_RIGHT:
                self.pData.incVelocity(Physics.Vector2D(1, 0))
            elif i == CONTROLLER_TRIGGER:
                if self.lastShot > self.shotFrequency:
                    self.shoot()
                    self.lastShot = 0.0
        self.lastShot += 0.04
        self.pData.fullSpeed()
        Object.update(self, time);
    
    
    def shoot(self):
        shot = Shot(self.world, self.pData.position.add(Physics.Vector2D(0, -60)), self.shotImg)
        shot.pData.velocity = Physics.Vector2D(0, -20)
        self.world.addObject(shot)
    
    def kill(self):
        self.goingToDie = True
        self.pData.intangible = True
#--------------------------------------------------------------------------------------------------------
 
#----------------------------------------------------------- Player Ship --------------------------------    
class PlayerShip(Ship):
    '''
    Classe que representa a nave do jogador.
    '''
    
    def __init__(self, world, img, killImgs, shotImg=None):
        Ship.__init__(self, world, img, killImgs)
        self.score = 0
        self.pData.colRect = (40, 40)
        self.shotFrequency = 0.4
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------- Enemy Ship -----------------------------------
class EnemyShip(Ship):
    def __init__(self, world, img, group, killImgs):
        Ship.__init__(self, world, img, killImgs)
        self.pData.colRect = (50, 50)
        self.pData.mass = 6000
        self.ai = AI(self, world)
        self.group = group;
        self.pData.MAX_SPEED = 5
        self.shotFrequency = 0.8
    
    def update(self, time):
        Ship.update(self, time)
        self.ai.update()
    
    def shoot(self):
        shot = Shot(self.world, self.pData.position.add(Physics.Vector2D(0, 60)), self.shotImg)
        shot.pData.velocity = Physics.Vector2D(0, 20)
        self.world.addObject(shot)
#--------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------- "AI" ----------------------------------

class AI:
    '''
    AI. Os movimento são atualizados
    aleatoriamente a cada 12 frames.
    Quando a nave estiver em rota de colisão
    com outra nave do mesmo grupo, a AI
    irá emitir um controle na direção oposta
    à rota. Isso evita colisões entre naves
    inimigas, mas não entre tiros ou naves
    de grupos diferentes.
    '''
    def __init__(self, ship, world):
        self.ship = ship
        self.world = world
        self.directions = []
        self.msgs = []
        self.directions.append(CONTROLLER_DOWN)
        self.directions.append(CONTROLLER_LEFT)
        self.directions.append(CONTROLLER_RIGHT)
        self.directions.append(CONTROLLER_UP)
        self.directions.append(CONTROLLER_TRIGGER)
        self.direction = CONTROLLER_DOWN
        self.counter = 0
        self.shoot = 0
    
    def update(self):
        if self.counter > 12:
            self.counter = 0
            self.ship.controlPanel.control_release(self.direction)
            self.direction = self.directions[random.randint(0, 3)]
            self.ship.controlPanel.control_input(self.direction)
        self.shoot = random.randint(0, 1)
        for ship in self.ship.group:
            if ship == self.ship:
                continue
            if self.ship.pData.position.distance(ship.pData.position) < 100:
                tmp = self.ship.pData.position.oppose(ship.pData.position)
                if tmp.x < 0:
                    self.ship.controlPanel.control_input(CONTROLLER_LEFT)
                elif tmp.x > 0:
                    self.ship.controlPanel.control_input(CONTROLLER_RIGHT)
                if tmp.y < 0:
                    self.ship.controlPanel.control_input(CONTROLLER_UP)
                elif tmp.y > 0:
                    self.ship.controlPanel.control_input(CONTROLLER_DOWN)
            if self.ship.pData.isBelowAndInFront(ship.pData):
                self.shoot = -1;
        self.ship.pData.fullSpeed()
        if self.shoot == 1:
            self.ship.controlPanel.control_input(CONTROLLER_TRIGGER)
        else:
            self.ship.controlPanel.control_release(CONTROLLER_TRIGGER)
        self.counter += 1
        
#--------------------------------------------------------- Shot -----------------------------------------
class Shot(Object):
    '''
    Classe geradora de tiros. Recebe uma imagem
    como par�metro. Imagem que ser� usada subsequshemdfy... ...mente.
    '''
    def __init__(self,  world, position=Physics.Vector2D(), img=None):
        Object.__init__(self, world, img)
        self.pData.colRect = (2, 6)
        self.pData.dimension = world.size
        self.pData.position = position
        self.pData.MAX_SPEED = 50;
        self.pData.contained = False
        self.pData.type = "Shot"
    
    def update(self, time):
        Object.update(self, time)
        self.pData.fullSpeed()
#-------------------------------------------------------------------------------------------------------

#--------------------------------------------------------- Score ---------------------------------------
