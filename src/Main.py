# -*- coding: utf-8 -*-

'''
Created on Dec 7, 2011

@author: Helison Reus e Wolmir Nemitz
'''

import pygame, sys, Screens
import GameWorld
from pygame.locals import QUIT
from pygame.locals import K_ESCAPE
from pygame.locals import KEYUP
from pygame.locals import KEYDOWN

SIZE = (600, 700)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
world = GameWorld.World(SIZE)
scrManager = Screens.ScreenManager()
scrManager.currentScreen = Screens.StartScreen(SIZE, scrManager)
#scrManager.currentScreen = Screens.ScoreTestScreen(SIZE, scrManager)
seconds = 0.0
imgCounter = 0;
BLACK = (0, 0, 0)

while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if not hasattr(event, 'key'): continue
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            scrManager.currentScreen.control_input(event.key)
                
        elif event.type == KEYUP:
            scrManager.currentScreen.control_release(event.key)
    
    scrManager.currentScreen.update(seconds)
    screen.fill(BLACK)
    scrManager.currentScreen.draw(screen)
    pygame.display.flip()
    #pygame.image.save(screen, "screenshots\scr" + str(imgCounter) + ".png")
    imgCounter += 1
    seconds += 0.040
    clock.tick(24)
    #clock.tick(1)