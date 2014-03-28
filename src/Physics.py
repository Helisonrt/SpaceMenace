# -*- coding: utf-8 -*-
'''
Created on Nov 19, 2011

@author: Wolmir Nemitz
'''

import math

class Vector2D(object):
    '''
    Classe para representar um vetor 2D e opera��es
    simples sobre ele.
    '''


    def __init__(self, x=0.0, y=0.0):
        '''
        Constructor.
        Recebe como par�metros as suas coordenadas iniciais.
        '''
        self.x = x
        self.y = y
    
    def reverse(self):
        '''
        M�todo que retorna um vetor com
        sentido oposto a este.
        '''
        return Vector2D(-self.x, -self.y)
        
    def length(self):
        '''
        Retorna a magnitude do vetor. Seu comprimento.
        '''
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def squaredLength(self):
        '''
        Retorn a magnitude do vetor, sem executar uma radicia��o,
        para fins de desempenho. E porque o cara do livro disse pra
        fazer assim. Da� eu digo am�m.
        '''
        return (self.x * self.x + self.y * self.y)
    
    def normalize(self):
        '''
        Retorna um vetor com exatamente o mesmo sentido
        deste, mas de comprimento unit�rio.
        '''
        l = self.length()
        if l > 0.0:
            return Vector2D(self.x / l, self.y / l)
        return Vector2D()
    
    def scalarMult(self, scalar):
        '''
        Retorna um novo vetor que � a multiplica��o deste por
        um escalar.
        '''
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def addScalar(self, scalar):
        '''
        Retorna um vetor que representa um vetor resultante da
        adi��o deste com um escalar.
        '''
        return Vector2D(self.x + scalar, self.y + scalar)
    
    def add(self, v):
        '''
        Retorn um vetor resultante da adi��o deste com outro vetor
        '''
        return Vector2D(self.x + v.x, self.y + v.y)
    
    def scalarProduct(self, v):
        '''
        Retorna o produto escalar deste vetor com outro vetor.
        '''
        return (self.x * v.x + self.y + v.y)
    
    def angle(self, v):
        '''
        Retorn o �ngulo deste vetor com o vetor passado como par�metro.
        Para achar o �ngulo deste vetor em rela��o a um dos eixos,
        basta fazer angle(Vector2D(0, 1)), para Y, angle(Vector2D(1, 0))
        para X.
        '''
        return math.acos(self.normalize().scalarProduct(v.normalize()))
    
    def distance(self, v):
        '''
        Calcula a distancia entre a ponta final de dois vetores.
        '''
        return v.add(self.reverse()).length()
    
    def oppose(self, v):
        return self.add(v.reverse())
    


class PhysicsData:
    '''
    Cont�m as informa��es utilizadas para atulizar a parte f�sica dos objetos.
    '''
    def __init__(self, colRect, dimension):
        self.velocity     = Vector2D()
        self.acceleration = Vector2D()
        self.position     = Vector2D()
        self.colRect = colRect
        self.dimension = dimension
        self.lastCollision = -1.0
        self.mass = 1.0;
        self.MAX_SPEED = 0.0
        self.MAX_ACC = 0.0;
        self.contained = True
        self.dead = False
        self.type = ""
        self.intangible = False
        
    def update(self, time):
        '''
        Atualiza a posi��o, utilizando uma integra��o diferente. Em vez da formula cl�ssica,
        atualizamos primeiro a posi��o e depois a velocidade.
        '''
        
        self.position = self.position.add(self.velocity)
        self.velocity = self.velocity.add(self.acceleration)
        self.velocity = self.velocity.normalize().scalarMult(self.MAX_SPEED)
        if self.position.x < 0:
            if self.contained:
                self.position.x = 0
            else:
                self.dead = True
        if self.position.x > self.dimension[0]:
            if self.contained:
                self.position.x = self.dimension[0]
            else:
                self.dead = True
        if self.position.y < 0:
            if self.contained:
                self.position.y = 0
            else:
                self.dead = True
        if self.position.y > self.dimension[1]:
            if self.contained:
                self.position.y = self.dimension[1]
            else:
                self.dead = True
        
        
    def collide(self, pData, time):
        #if (self.lastCollision == time) or (pData.lastCollision == time):
            #return False
        if self.intangible:
            return False
        sx1 = self.position.add(Vector2D(-self.colRect[0] / 2, 0)).x
        sx2 = sx1 + self.colRect[0]
        sy1 = self.position.add(Vector2D(0, -self.colRect[1] / 2)).y
        sy2 = sy1 + self.colRect[1]
        
        px1 = pData.position.add(Vector2D(-pData.colRect[0] / 2, 0)).x
        px2 = px1 + pData.colRect[0]
        py1 = pData.position.add(Vector2D(0, -pData.colRect[1] / 2)).y
        py2 = py1 + pData.colRect[1]
        
        if (sx1 <= px2) and (sx2 >= px1):
            if (sy1 <= py2) and (sy2 >= py1):
                return True
        return False
    
    def incVelocity(self, velocity):
        self.velocity = self.velocity.add(velocity)
        if self.velocity.length() > self.MAX_SPEED:
            self.fullSpeed()
            
    def incAcceleration(self, acc, fullAcc):
        self.acceleration = self.acceleration.add(acc)
        if self.acceleration.length() > self.MAX_ACC or fullAcc == True:
            self.acceleration = self.acceleration.normalize().scalarMult(self.MAX_ACC)
            
    def fullSpeed(self):
        self.velocity = self.velocity.normalize().scalarMult(self.MAX_SPEED)
        
    '''def repulse(self, target):
        #tmp = self.position.oppose(target.position).squaredLength()
        #tmp = self.position.oppose(target.position).normalize().scalarMult(100)
        #if tmp <= 0:
            #tmp = 1
        #self.velocity = self.velocity.add(self.position.oppose(target.position).normalize().scalarMult((self.mass * target.mass) / tmp))
        #self.velocity = self.velocity.add(tmp)
        #print self.velocity.x
        self.velocity = self.velocity.add(Vector2D(100, 0))'''
    
    def isBelowAndInFront(self, pData):
        return self.position.y < pData.position.y and math.fabs(self.position.x - pData.position.x) < 140 