#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 08:01:46 2024

@author: timsowinski
"""

import pygame
import math
import sys
from datetime import datetime, timedelta

pygame.init()

# constants are written in capitals
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("Lato", 30)


class Planet():
    
    # defines constants
    AU = 149.6e6 * 1000 # astronomical units in meters
    G = 6.67428e-11 # gravitational constant
    SCALE = 200/AU # sets the scale so 1AU ~100 pixels
    TIMESTEP = 3600*24 # seconds in a day, don't want to simulate each second as this would take ages
    
    
    # sets the initialisation values of the planet
    def __init__(self, x, y, radius, colour, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass
        self.name = name
        
        self.orbit = [] # will be a list of all the points the planet has travelled on, so we can draw it
        self.sun = False # this is used to draw the orbit of planets, if it isn't the sun
        self.distance_to_sun = 0
        
        self.x_vel = 0 # x velocity
        self.y_vel = 0 # y velocity
        
    def draw(self, win): # function to draw planets onto the window
        
        # in pygame, (0, 0) is the top left of the screen
        # therefore, any positions will need to be offset by the width/height /2 
        # then they will be in the middle of the screen 
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        
        n = 40
        
        if len(self.orbit) > 2: # need at least 3 points to draw a line
            updated_points = []
            for point in self.orbit:
                x, y = point
            
                # normalises x, y values to the middle
                x = x*self.SCALE + WIDTH/2
                y = y*self.SCALE + HEIGHT/2
                
                updated_points.append((x, y))
                
            if len(updated_points) <= n:
                pygame.draw.lines(win, self.colour, False, updated_points, 2)
            else:
                pygame.draw.lines(win, self.colour, False, updated_points[len(updated_points) - n:], 2)                
        else:
            pass
        
        pygame.draw.circle(win, self.colour, (x, y), radius = self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1.6e9, 2)} billion miles", 4, WHITE)
            name_text = FONT.render(f"{self.name}", 4, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/3))
            win.blit(name_text, (x - 25, y + distance_text.get_width()/5))
    def attraction(self, other): # other = other planet
        # gets distance values of other object
        other_x, other_y = other.x, other.y
        
        # finds cartesian distance between planets
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        
        # straight line distance between them
        distance = math.sqrt((distance_x ** 2) + (distance_y ** 2))
        
        if other.sun == True:
            self.distance_to_sun = distance # sets distance to sun as distance
        
        # straight line force
        force = (self.G * self.mass * other.mass)/distance**2
        
        # need to break down force into x and y components
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
        
    def update_position(self, planets: list):
        total_fx = total_fy = 0 # sets total force in x and y to 0
        
        # for loop adds total force in x and y from all the planets in the list of planets
        for planet in planets:
            # if planet = self, we want to pass otherwise the code will break due to div0
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        
        # below constantly updates the x and y velocities by timestep
        self.x_vel += (total_fx/self.mass) * self.TIMESTEP 
        self.y_vel += (total_fy/self.mass) * self.TIMESTEP 
        
        # below constantly updates the x and y positions
        #self.x += self.x_vel * self.TIMESTEP / self.SCALE
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y)) # appends previous positions of the planet
        
        # print(f"{self.name} - {planet.name}: {total_fx}")
        # print(f"{self.name} - {planet.name}: {total_fy}")

        #print(f"{self.name} - {planet.name}: {self.orbit}")
        
        
def main() -> None:
    start_time = datetime.now()
    run = True
    
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 30, YELLOW, 1.988*10**30, "Sun")
    sun.sun = True
    
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24, "Earth")
    earth.y_vel = 29.783*1000 # starting y velocity (just empirical number in m/s)
    # earth.x_vel = 29.783*1000 # starting y velocity (just empirical number in m/s)
    
    mars = Planet(-1*1.524*Planet.AU, 0, 12, RED, 2.39*10**23, "Mars")
    mars.y_vel = 24.077*1000
    
    mercury = Planet(-1*0.387*Planet.AU, 0, 8, DARK_GREY, 0.330*10*24, "Mercury")
    mercury.y_vel = 47.4*1000
    
    venus = Planet(-1*0.723*Planet.AU, 0, 14, WHITE, 4.86*10**24, "Venus")
    venus.y_vel = 35.02*1000
    
    planets = [sun, earth, mars, mercury, venus]
    
    
    while run == True:
        clock.tick(60) # sets a maximum refresh rate of 60Hz
        WIN.fill((0, 0, 0)) # refreshs the screen to black, needed to overwrite previous planet positions
        # for loop tracks all events in the game, like mouse clicks, keyboard clicks etc
        for event in pygame.event.get():
            # if the event is clicking the exit button, closes the window
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            """
            if planet.name == "Earth":
                #print(f"{planet.name}: x = {planet.x/planet.AU:.3f}, y = {planet.y/planet.AU:.3f}")
                #print(f"{planet.name}: x = {planet.x_vel}, y_vel = {planet.y_vel}")
            """
            planet.draw(WIN)
        #sys.exit()
        pygame.display.update() # updates the screen with new updates since the previous update
    # pygame.display.quit()
    pygame.quit()
    print(f"Animation ended after {(datetime.now() - start_time).total_seconds()}s")
    
    # sys.exit(0)

main()

