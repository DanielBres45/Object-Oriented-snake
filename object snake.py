# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:22:13 2018

@author: Daniel

First uploaded version. Sorry I am new to version checking
"""

import pygame
import random

class game():
    #initialize game variables
    #no spaces in parenthesis
    white = (255,255,255)
    black = (0,0,0)
    white = (255,255,255)
    red = (255, 0, 0)
    display_width = 500
    display_height = 500
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
        
    #this function checks to see if any one objects pixels values are inside of another objects pixel values
    def overlap(self, selfx, selfy, selfSize, size, X, Y):
        
        if ((selfx > X and selfx < X + size or selfx+selfSize > X and selfx + selfSize < X + size) and ((selfy > Y and selfy < Y + size or selfy+selfSize > Y and selfy + selfSize < Y + size))):
            return True
        else:
            return False
   
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
            if self.overlap(cherry.x, cherry.y, cherry.size, Python.size, Python.body[0][0], Python.body[0][1]):
                Python.score += 1
                Python.update()
                cherry.update()
            
            #check to see if the head touches the border 
            if (Python.body[0][0] > self.display_width - Python.size or Python.body[0][0] < 0 or Python.body[0][1] > self.display_height - Python.size or Python.body[0][1] < 0):
                self.die(self.gameDisplay)
                
            #check to see if the head is inside the body at any point
            for x, i in enumerate(Python.body):
                if x > 3:
                    if self.overlap(Python.body[0][0], Python.body[0][1], Python.size, Python.size, i[0], i[1]):
                        self.die(self.gameDisplay)
                     
#            original collision checking, only saw if the entire head overlapped the body            
#            if (Python.body[0] in Python.body[1:-1]):
#                self.die(self.gameDisplay) 
            
            #I have an extra if statement because the crash happens before the update, so sometimes
            #it tries to update even though the game ended
            if not self.crashed:
                pygame.display.update()
                
            self.clock.tick(60)
            
        
        
                
        
        
class snake(game):
    
    def __init__(self, game):
        self.length = 3
        self.last = pygame.time.get_ticks()
        self.size = 20
        self.step = 2
        self.score = 0
        self.body = [[game.display_width/2, game.display_height/2], [game.display_width/2 - 80, game.display_height], [game.display_width/2 - 100, game.display_height]]
        self.direction = 0
    
    #update function is called every time you score a point
    #this function appends an extra body piece to the end of the snake 
    def update(self):
        self.body.append([self.body[-1][0], self.body[-1][1]])
        self.length += 1
      
    #This funciton moves the snake by taking the head and adding a constant to either the x or the y
    #moving the rest of the body happens at draw
    def main_loop(self):
        now = pygame.time.get_ticks()
        if (now - self.last) >= 160:
            self.last = now
            for i in range(self.length-1,0,-1):
                self.body[i] = self.body[i - 1]
        if self.direction == 0:
            self.body[0] = [self.body[0][0] + self.step, self.body[0][1]]
        if self.direction == 1:
            self.body[0] = [self.body[0][0] - self.step, self.body[0][1]]
        if self.direction == 2:
            self.body[0] = [self.body[0][0] , self.body[0][1] - self.step]
        if self.direction == 3:
            self.body[0] = [self.body[0][0], self.body[0][1] + self.step]
            
    def moveRight(self):
        self.direction = 0
        
    def moveLeft(self):
        self.direction = 1
        
    def moveUp(self):
        self.direction = 2
        
    def moveDown(self):
        self.direction = 3 
        
    #this is the actual function that creates the snake like body, for every part of the snake
    #it makes its value the previous one, making a trailing effect
    def draw(self, surface, game):
        for i in range(len(self.body)):
            pygame.draw.rect(surface, game.white, ((self.body[i][0],self.body[i][1]),(self.size,self.size)))
    
    def getScore(self):
        return self.score
    
#the only fantastic part about the cherry is the fact that its coordinates are randomly generated
class pointCherry(game):
    
    def __init__(self, game):
        self.size = 15
        self.x = random.randint(20, game.display_width - self.size)
        self.y = random.randint(20, game.display_height - self.size)
        self.rect = pygame.rect.Rect((self.x, self.y),(self.size, self.size))
        self.red = game.red
        
    def update(self):
        self.x = random.randint(20, game.display_width - self.size)
        self.y = random.randint(20, game.display_height - self.size)
        
    def draw(self, surface):
        self.rect = pygame.rect.Rect((self.x, self.y),(self.size, self.size))
        pygame.draw.rect(surface, self.red, self.rect)
        
Game = game()
Python = snake(Game)
cherry = pointCherry(Game)

Game.game_loop(Python, cherry)

