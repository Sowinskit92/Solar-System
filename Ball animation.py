#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 12:01:06 2024

@author: timsowinski
"""

import pygame
from datetime import datetime, timedelta
from random import random, randint
import sys
pygame.init()


WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball animation")


class Ball():
    
    def __init__(self, colour, x, y, name = False, radius = 20, x_vel = False, y_vel = False):
        self.colour = colour
        self.x = x/2
        self.y = y/2
        self.radius = radius
        self.mass = 5*self.radius
        
        if x_vel == False:
            self.x_vel = randint(5, 20)
        else:
            self.x_vel = x_vel
        
        if y_vel == False:
            self.y_vel = randint(5, 20)
        else:
            self.y_vel = y_vel
        
        self.x_direction = 1
        self.y_direction = 1
        self.x_force = 0
        self.y_force = 0
    
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        
        
    def update_position(self, balls):
        
        for ball in balls:
            
            if self == ball:
                continue
            else: # x collisions with other balls
                if ball.x < (self.x + self.radius):
                    self.x_direction = -1*self.x_direction
                    #ball.x_direction = -1*ball.x_direction
                """
                if (ball.x >= self.x - self.radius) or (ball.x <= self.x + self.radius):
                    self.x_vel = (ball.mass * ball.x_vel)/self.mass
                    ball.x_vel = (self.mass * self.x_vel)/ball.mass
                    run = False"""
    
            
        """X collisions with walls"""
        if self.x <= 0 + self.radius:
            self.x_direction = 1
        elif self.x >= WIDTH - self.radius:
            self.x_direction = -1
        else:
            pass
        
        """Y collisions with walls"""
        if self.y <= 0 + self.radius:
            self.y_direction = 1
        elif self.y >= HEIGHT - self.radius:
            self.y_direction = -1
        
        
        self.x += self.x_direction * self.x_vel
        #self.y += self.y_direction * self.y_vel
        


def main(nballs = 5):
    run = True
    clock = pygame.time.Clock()
    
    ball1 = Ball(colour = (179, 235, 242), x = 200, y = 100, x_vel = 10, y_vel = 0)
    ball2 = Ball(colour = (255, 209, 220), x = 800, y = 100, x_vel = 10, y_vel = 0)
    balls = [ball1, ball2]
    #balls = [Ball(colour = (int(random()*255), int(random()*255), int(random()*255)), x = int(random()*WIDTH), y = int(random()*HEIGHT)) for i in range(nballs)]
    
    
    while run == True:
        
        clock.tick(5)
        
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #ball.update_position(t = (datetime.now() - start_time).total_seconds())
        for i in balls:
            i.update_position(balls)
            i.draw(WIN)
        print(balls[0].x - balls[1].x)
        pygame.display.update()
    pygame.quit()
    
main(10)






"""G = 100

class Ball():
    def __init__(self, colour, x, y, radius = 20):
        self.colour = colour
        self.x = x
        self.y = y
        self.radius = radius
        
        self.y_vel = 10
        
        
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.y_vel += G
        self.y += self.y_vel
        
        
        

def main():
    run = True
    start_time = datetime.now()
    ball = Ball(colour = (179, 235, 242), x = 300, y = 200)

    while run == True:
        
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        ball.move()
        ball.draw(WIN)
        print(ball.x, ball.y)
        
        pygame.display.update()
    pygame.quit()
    
main()"""













"""class Ball():
    
    def __init__(self, colour, x, y, radius = 20):
        self.colour = colour
        self.x = x
        self.y = y
        self.radius = radius
        
        self.x_vel_init = -100
        self.test_var = "boom"
        self.y_vel = 0
        self.x_vel_list = []
        self.y_vel_list = []
    
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        
        
    def update_position_old(self, t):
        
        if (self.x <= 100):
            self.x_direction = 1
        elif (self.x >= 600):
            self.x_direction = -1
        else:
            pass
        
        self.x += self.x + (self.x_direction * self.x_vel * t)
        #self.y += self.y + (self.y_vel * t)
        
        
    def test(self, t):
        
        x_vel = self.x_vel_init
        
        if self.x < 200:
            t = -t
            
        self.x += self.x + (x_vel * t)


def main():
    run = True
    start_time = datetime.now()
    while run == True:
        
        ball = Ball(colour = (179, 235, 242), x = 300, y = 100)
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #ball.update_position(t = (datetime.now() - start_time).total_seconds())
        ball.test(t = (datetime.now() - start_time).total_seconds())
        ball.draw(WIN)
        print(ball.x, ball.test_var)
        
        pygame.display.update()
    pygame.quit()
    
main()"""
