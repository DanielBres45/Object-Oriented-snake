# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:22:13 2018

@author: Daniel
"""

import pygame
import random
import time

class game():
    #initialize game variables
    #no spaces in parenthesis
    white = (255,255,255)
    black = (0,0,0)
    white = (255,255,255)
    red = (255, 0, 0)
    display_width = 700
    display_height = 700
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    crashed = False
    
    def __init__(self):
        #__init __ doesnt initialize the game class, but actually pygame 
        pygame.init()    
        pygame.display.set_caption('snake')
        self.clock = pygame.time.Clock()  
        
    #text_object and message display are responsible for all text handeling 
    def text_objects(self, text, font):
        
        textSurface = font.render(text, True, self.white)
        return textSurface, textSurface.get_rect()
    
    def message_display(self, text, size, location):
        
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = location
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        
   
    #end the game if dead     
    def die(self, surface):
        
        self.crashed = True    
        pygame.quit()
        
        
        
    def game_loop(self, Python, cherry):
        

        while not self.crashed:
            #this is the handeling loop, that handles all keyboard output
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    pygame.quit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        #the reason that snake has functions for direction instead of just doing it here, is because everything is object, I dont want to have to pass everything again
                        Python.moveLeft()
                       
                    elif event.key == pygame.K_RIGHT:
                        Python.moveRight()
                        
                    elif event.key == pygame.K_UP:
                        Python.moveUp()
                       
                    elif event.key == pygame.K_DOWN:
                        Python.moveDown()
                        
            #basically blank the screen refresh it
            self.gameDisplay.fill(self.black)  
            
            #draw everything 
            cherry.draw(self.gameDisplay)  
            Python.draw(self.gameDisplay, game)
            self.message_display(format("Score: %d" % (Python.length - 3)), 20, (40, 15) )
            
            #change the direction of the "Snake"
            Python.main_loop() 
            
            
            #once again call the overlap function to see if the snake and cherry overlap every frame
            if Python.is_collided_with(cherry.rect):
                Python.score += 1
                Python.update()
                cherry.update()
            
#            if self.overlap(cherry.x, cherry.y, cherry.size, Python.size, Python.body[0][0], Python.body[0][1]):
#                Python.score += 1
#                Python.update()
#                cherry.update()
            
            #check to see if the head touches the border 
            if (Python.body[0][0] > self.display_width - Python.size or Python.body[0][0] < 0 or Python.body[0][1] > self.display_height - Python.size or Python.body[0][1] < 0):
                self.die(self.gameDisplay)
                
            #check to see if the head is inside the body at any point
            for i in Python.body[3:]:
                if Python.is_collided_with(i):
                    self.die(self.gameDisplay)
                
                     
            
            #I have an extra if statement because the crash happens before the update, so sometimes
            #it tries to update even though the game ended
            if not self.crashed:
                pygame.display.update()
                
            #self.clock.tick(120)
            time.sleep(.1)
            
        
        
                
        
        
class snake(game):
    """
    Changed snake to use pygame rects for all body pieces, instead of being deifned as points
    Makes everyhting more effiecient
    """
    
    
    def __init__(self, game):
        self.length = 3
        self.last = pygame.time.get_ticks()
        self.size = 20
        self.step = 20
        self.score = 0
        self.body= [pygame.Rect((game.display_width/2, game.display_height/2), (20, 20)), pygame.Rect((game.display_width/2 + 30, game.display_height/2), (20, 20)), pygame.Rect((game.display_width/2 + 50, game.display_height/2), (20, 20))]
#        self.body = [[game.display_width/2, game.display_height/2], [game.display_width/2, game.display_height], [game.display_width/2 , game.display_height]]
        self.direction = 1
        self.lastMove = 1
        
    
    #update function is called every time you score a point
    #this function appends an extra body piece to the end of the snake 
    def update(self):
        self.body.append(self.body[-1])
        self.length += 1
      
    #changed this function to use the built in pygame moveRect function
    #moving the rest of the body happens at draw
    
    def main_loop(self):
        now = pygame.time.get_ticks()
        if (now - self.last) >= 60:
            self.last = now
            #reverse for loop
            for i in range(self.length-1,0,-1):
                self.body[i] = self.body[i - 1]
        
        #right
        if self.direction == 0:
            if self.lastMove == 1:
                #if left, keep left
                self.body[0] = self.body[0].move(-self.step, 0)
                self.lastMove = 1
                
            else:
                self.body[0] = self.body[0].move(self.step, 0)
                self.lastMove = 0
            
        #left
        if self.direction == 1:
            if self.lastMove == 0:
                #if right, keep right
                self.body[0] = self.body[0].move(self.step, 0)
                self.lastMove = 0
                
                
            else:
                self.body[0] = self.body[0].move(-self.step, 0)
                self.lastMove = 1
        
        #up
        if self.direction == 2:
            if self.lastMove == 3:
                #if down keep down
                self.body[0] = self.body[0].move(0, self.step)
                self.lastMove = 3
                
                
            else:
                self.lastMove = 2
                self.body[0] = self.body[0].move(0, -self.step)
            
        #dowm
        if self.direction == 3:
            if self.lastMove == 2:
                self.body[0] = self.body[0].move(0, -self.step)
                self.lastMove = 2
                
                
            else:
                self.body[0] = self.body[0].move(0, self.step)
                self.lastMove = 3
            
    def moveRight(self):
        self.direction = 0
        
    def moveLeft(self):
        self.direction = 1
        
    def moveUp(self):
        self.direction = 2
        
    def moveDown(self):
        self.direction = 3 
        
    def is_collided_with(self, rect):
        return self.body[0].colliderect(rect)
        
    #this is the actual function that creates the snake like body, for every part of the snake
    #it makes its value the previous one, making a trailing effect
    def draw(self, surface, game):
        for i in range(len(self.body)):
            pygame.draw.rect(surface, game.white, self.body[i])
    
    def getScore(self):
        return self.score
    
#the only fantastic part about the cherry is the fact that its coordinates are randomly generated
class pointCherry(game):
    
    def __init__(self, game):
        self.size = 15
        self.x = random.randint(20, game.display_width - self.size)
        self.y = random.randint(20, game.display_height - self.size)
        self.rect = pygame.rect.Rect((self.x, self.y),(self.size, self.size))
        
    def update(self):
        self.x = random.randint(20, game.display_width - self.size)
        self.y = random.randint(20, game.display_height - self.size)
        self.rect = pygame.rect.Rect((self.x, self.y),(self.size, self.size))
        
    def draw(self, surface):
        
        pygame.draw.rect(surface, game.red, self.rect)
        
Game = game()
Python = snake(Game)
cherry = pointCherry(Game)
Game.game_loop(Python, cherry)

