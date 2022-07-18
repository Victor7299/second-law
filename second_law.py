import pygame
import pymunk
import random

import numpy as np
import pandas as pd
import math

pygame.init()

#Un px = 8cm

display = pygame.display.set_mode((420, 650))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 50
kb = 1.380649E-23

def convert_coordinates(point):
    return int(point[0]), 600-int(point[1])

class Ball():
    def __init__(self, x, y, collision_type, up = 1):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = 150 , -156            #velocida en 1px/s
        # self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)
        # self.body.velocity = 0, up*100
        self.shape = pymunk.Circle(self.body, 1)
        self.shape.elasticity = 1
        self.shape.density = 1.066630334E-26       #Escogiendo de modelo el gas neon kg/px3
        self.shape.collision_type = collision_type
        space.add(self.body, self.shape)
    def draw(self):
        if self.shape.collision_type != 2:
            pygame.draw.circle(display, (255, 0, 0), self.body.position, 1)
        else:
            pygame.draw.circle(display, (0, 0, 255), self.body.position, 1)
    # def change_to_blue(self, arbiter, space, data):
    #     self.shape.collision_type = 2

class Wall():
    def __init__(self,p1,p2,collision_number=None):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.shape = pymunk.Segment(self.body,p1,p2,5)
        self.shape.elasticity = 1
        space.add(self.body,self.shape)
        if collision_number:
            self.shape.collision_type = collision_number

    def draw(self):
        pygame.draw.line(display,(0,0,0),self.shape.a, self.shape.b,5)
        
def mod_velocity(v):
    return (v[0]**2+v[1]**2)**0.5

def bar(x,y,w,h):
    yn = y - h
    pygame.draw.rect(display,(120,120,120),(x,yn,w,h))
    pygame.draw.rect(display,(255,255,255),(x,yn,w,h),2)

def statistics(datos):
    k = 1 + 3.322 * math.log10(len(datos))
    numero = int(k)
    if numero % 2 == 0:
        periods = math.ceil(k)
    else:
        periods = int(k)
    inf = 0        # Limite inferior del primer intervalo
    sup = 330    # Limite superior del último intervalo
    
    intervals = pd.interval_range(
        start=inf,
        end=sup,
        periods=periods,
        name="Intervalo",
        closed="left")
    df = pd.DataFrame(index=intervals)
    df["FreqAbs"] = pd.cut(datos, bins=df.index).value_counts()
    df["Marca"]  = df.index.mid
    a = df["FreqAbs"].values
    rms = np.mean(df["FreqAbs"]**2)**0.5 #la root mean square
    return a , periods, rms


font = pygame.font.Font("FiraCode.ttf", 15)

texty = font.render('#Partículas',False,'#000000')
textx = font.render('Velocidad',False,'#000000')

pygame.display.set_caption('2da Ley de Termodinámica')

# programIcon = pygame.image.load('logo-unsaac-nav.ico')

# pygame.display.set_icon(programIcon)
        
def game():
    balls = [Ball(random.randint(120, 300), random.randint(120, 300), i+3) for i in range(500)]
    # balls.append(Ball(400, 400, 2))
    walls = [Wall([20,20],[20,400]), Wall([18,20],[402,20]), Wall([400,20],[400,400]),Wall([18,400],[402,400])]

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        [wall.draw() for wall in walls]
        [ball.draw() for ball in balls]
        v = np.array([mod_velocity(ball.body.velocity) for ball in balls])
        v.sort()
        feq, period, rms = statistics(v)
        heights = [ufeq/feq.max()*190 for ufeq in feq]
        [bar(30+i*int(360/period), 600, int(360/period), heights[i]) for i in range(period)]
        pygame.draw.line(display,(0,0,0),(20,410),(20,610),2)
        pygame.draw.line(display,(0,0,0),(10,600),(410,600),2)
        display.blit(texty,(25,410))
        display.blit(textx,(325,605))
        m = balls[1].body.mass
        vp = rms*10
        T = vp**2*m/(2*kb)
        # pygame.time.wait(500)
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()
pygame.quit()






















