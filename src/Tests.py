# -*- coding: utf-8 -*-
'''
Created on Jan 6, 2012

@author: Wolmir Nemitz
'''
import GameWorld, pygame, Physics, pygame.locals

'''
Deu erro na movimentacao. Era necessario dar dois updates
para a nave mudar a posicao.
'''
class MovementTest:
    def __init__(self):
        self.world = GameWorld.World((800, 800))
        self.playerShipImage = pygame.image.load('PlayerShip.png')
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
        
    
    def test(self):
        #Primeiro os testes gerais.
        print("Testes de Movimentos:")
        # Teste 1: Esquerda
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_LEFT)
        self.world.update(0.0)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x < tmpPos.x) and (tmpPos2.y == tmpPos.y):
            print "Left: True"
        else:
            print "Left: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_LEFT)
        #Teste 2: Direita
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_RIGHT)
        self.world.update(0.04)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x > tmpPos.x) and (tmpPos2.y == tmpPos.y):
            print "Right: True"
        else:
            print "Right: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_RIGHT)
        #Teste 3: Para Cima:
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_UP)
        self.world.update(0.08)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x == tmpPos.x) and (tmpPos2.y < tmpPos.y):
            print "Up: True"
        else:
            print "Up: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_UP)
        #Teste 4: Para Baixo:
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_DOWN)
        self.world.update(0.12)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x == tmpPos.x) and (tmpPos2.y > tmpPos.y):
            print "Down: True"
        else:
            print "Down: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_DOWN)
        #Teste 5: Para cima e para a esquerda.
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_UP)
        self.playerShip.controlPanel.control_input(pygame.locals.K_LEFT)
        self.world.update(0.16)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x < tmpPos.x) and (tmpPos2.y < tmpPos.y):
            print "Up and Left: True"
        else:
            print "Up and Left: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_UP)
        self.playerShip.controlPanel.control_release(pygame.locals.K_LEFT)
        #Teste 6: Para cima e para a direita.
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_UP)
        self.playerShip.controlPanel.control_input(pygame.locals.K_RIGHT)
        self.world.update(0.2)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x > tmpPos.x) and (tmpPos2.y < tmpPos.y):
            print "Up and Right: True"
        else:
            print "Up and Right: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_UP)
        self.playerShip.controlPanel.control_release(pygame.locals.K_RIGHT)
        #Teste 7: Para baixo e para a direita.
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_DOWN)
        self.playerShip.controlPanel.control_input(pygame.locals.K_RIGHT)
        self.world.update(0.24)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x > tmpPos.x) and (tmpPos2.y > tmpPos.y):
            print "Down and Right: True"
        else:
            print "Down and Right: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_DOWN)
        self.playerShip.controlPanel.control_release(pygame.locals.K_RIGHT)
        #Teste 8: Para baixo e para a esquerda.
        tmpPos = self.playerShip.pData.position
        self.playerShip.controlPanel.control_input(pygame.locals.K_DOWN)
        self.playerShip.controlPanel.control_input(pygame.locals.K_LEFT)
        self.world.update(0.28)
        tmpPos2 = self.playerShip.pData.position
        if (tmpPos2.x < tmpPos.x) and (tmpPos2.y > tmpPos.y):
            print "Down and Left: True"
        else:
            print "Down and Left: False"
        self.playerShip.controlPanel.control_release(pygame.locals.K_DOWN)
        self.playerShip.controlPanel.control_release(pygame.locals.K_LEFT)
        print()


class CollisionTest:
    def __init__(self):
        self.world = GameWorld.World((800, 800))
        self.playerShipImage = pygame.image.load('PlayerShip.png')
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
    
    
    def test(self):
        #Teste 1: Teste de nao-colisao.
        tst_obj1 = GameWorld.Object(self.world, None)
        tst_obj2 = GameWorld.Object(self.world, None)
        tst_obj1.pData.colRect = ()


MovementTest().test()