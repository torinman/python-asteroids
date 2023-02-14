#    asteroids3.py
#
#    A recreation from scratch of the classic arcade game. I've never actually
#    played the real game, so have based this on seeing youtube videos and
#    talking to people who have played it
#
#    The program requires PyGame and Python 3
#
#    Copyright (C) 2020-21  Torin Stephens
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see  <https://www.gnu.org/licenses/>.
from __future__ import division
import math
import random
import colorsys
import pygame
from pygame import Rect
from pygame.mixer import Sound
GAME__SPEED = 60
if __name__ == "__main__":
    with open('asteroids_high_score.txt', 'r') as f:
        highscore = int(f.read())
dead = False
asteroid_size = 2
SIZE = 703
angle = random.randint(0, 360)
rotateby = 0
positionx = SIZE/2
positiony = SIZE/2
thruston = False
speedx = 0
speedy = 0
bullets = []
mothership_bullets = []
mothership_bullet_counter = random.randint(10, 70)
mothership_disperse = False
mothership_offset = 57
mothership_direction_change_counter = random.randint(60, 120)
MOTHERSHIP_SIZE = 0.75
mothership_counter = random.randint(600, 900)
mothership_type = (mothership_counter % 2)+1
mothership_x = 0
mothership_y = random.randint(0, SIZE)
mothership_change_x = random.randint(-250, 250)/100
mothership_change_y = random.randint(-250, 250)/100
mothership_on = False
asteroids = []
randomdecition = 0
explodelines = []
explode = False
explodecounter = 0
asteroid_position_check = 0
asteroid_number = 0
score = 0
numberofasteroids = 4
lives = random.randint(3, 5)
extralifescounter = 0
def calculateGradient(p1, p2):
   if (p1[0] != p2[0]):
       m = (p1[1] - p2[1]) / (p1[0] - p2[0])
       return m
   else:
       return None
def calculateYAxisIntersect(p, m):
   return  p[1] - (m * p[0])
def getIntersectPoint(p1, p2, p3, p4):
   m1 = calculateGradient(p1, p2)
   m2 = calculateGradient(p3, p4)
   if (m1 != m2):
       if (m1 is not None and m2 is not None):
           b1 = calculateYAxisIntersect(p1, m1)
           b2 = calculateYAxisIntersect(p3, m2)   
           x = (b2 - b1) / (m1 - m2)       
           y = (m1 * x) + b1           
       else:
           if (m1 is None):
               b2 = calculateYAxisIntersect(p3, m2)   
               x = p1[0]
               y = (m2 * x) + b2
           elif (m2 is None):
               b1 = calculateYAxisIntersect(p1, m1)
               x = p3[0]
               y = (m1 * x) + b1           
           else:
               assert False
       return ((x,y),)
   else:
       b1, b2 = None, None
       if m1 is not None:
           b1 = calculateYAxisIntersect(p1, m1)
       if m2 is not None:   
           b2 = calculateYAxisIntersect(p3, m2)
       if b1 == b2:
           return p1,p2,p3,p4
       else:
           return None
def calculateIntersectPoint(p1, p2, p3, p4):
    p = getIntersectPoint(p1, p2, p3, p4)
    if p is not None:               
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]       
        r1 = Rect(p1, (width , height))
        r1.normalize()
        width = p4[0] - p3[0]
        height = p4[1] - p3[1]
        r2 = Rect(p3, (width, height))
        r2.normalize()  
        tolerance = 1
        if r1.width < tolerance:
            r1.width = tolerance   
        if r1.height < tolerance:
            r1.height = tolerance
        if r2.width < tolerance:
            r2.width = tolerance
        if r2.height < tolerance:
            r2.height = tolerance
        for point in p:                 
            try:    
                res1 = r1.collidepoint(point)
                res2 = r2.collidepoint(point)
                if res1 and res2:
                    point = [int(pp) for pp in point]                                
                    return point
            except:
                str = "point was invalid  ", point                
                print(str)
        return None            
    else:
        return None
class Explotion:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.angle = 0
        self.change_angle = 0
        self.length = 0
        self.counter = 0
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.xprev = 0
        self.yprev = 0
class Asteroid:
    def __init__(self):
        self.angle = 0
        self.anglechange = 0
        self.x = 0
        self.y = 0
        self.Size = 0
        self.takex = 0
        self.takey = 0
        self.changex = 0
        self.changey = 0
def make_explotion(x, y, changex, changey, angle, length):
    explosion = Explotion()
    explosion.x = x
    explosion.y = y
    explosion.change_x = changex
    explosion.change_y = changey
    explosion.angle = angle
    explosion.change_angle = random.randint(-1, 3)
    explosion.length = length
    explosion.counter = random.randint(20, 70)
    return(explosion)
def make_bullet():
    global positionx, positiony, angle
    bullet = Bullet()
    bullet.x = positionx
    bullet.y = positiony
    bullet.xprev = positionx + (math.cos(math.radians(angle))*20)
    bullet.yprev = positiony + (math.sin(math.radians(angle))*20)
    bullet.change_x = (math.sin(math.radians(angle))*7+speedx)
    bullet.change_y = (math.cos(math.radians(angle))*7+speedy)
    return bullet
def make_mothership_bullet():
    global mothership_x, mothership_y
    bullet = Bullet()
    bullet.x = mothership_x
    bullet.y = mothership_y
    bullet.xprev = mothership_x
    bullet.yprev = mothership_y
    bullet.change_x = 0
    bullet.change_y = 0
    return bullet
def make_asteroid(largeness, x_speed, y_speed, x, y, minusx, minusy):
    global randomdecition
    asteroid = Asteroid()
    asteroid.anglechange = random.randint(-100, 100)/100
    asteroid.x = x
    asteroid.y = y
    asteroid.Size = largeness
    asteroid.takex = minusx
    asteroid.takey = minusy
    asteroid.changex = x_speed
    asteroid.changey = y_speed
    return asteroid
def digits(number):
    tester = 10
    count = 0
    if number == 0:
        return(1)
    while True:
        count += 1
        if number < tester and number >= (tester/10):
            return(count)
        tester *= 10
def drawship():
    global angle, positionx, positiony, thruston, speedx, speedy
    angle = angle + rotateby
    positionx = positionx + speedx
    positiony = positiony + speedy
    speedx = speedx * 0.995
    speedy = speedy * 0.995
    if thruston == True:
        speedx = speedx + (math.sin(math.radians(angle))/20)
        speedy = speedy + (math.cos(math.radians(angle))/20)
        pygame.draw.line(screen, tuple(round(i * 255) for i in colorsys.hsv_to_rgb(random.randint(0, 17)/100,1,1)), (positionx + (math.sin(math.radians(angle+170))*10), positiony + (math.cos(math.radians(angle+170))*10)), (positionx + (math.sin(math.radians(angle+180))*20), positiony + (math.cos(math.radians(angle+180))*20)))
        pygame.draw.line(screen, tuple(round(i * 255) for i in colorsys.hsv_to_rgb(random.randint(0, 17)/100,1,1)), (positionx + (math.sin(math.radians(angle-170))*10), positiony + (math.cos(math.radians(angle-170))*10)), (positionx + (math.sin(math.radians(angle+180))*20), positiony + (math.cos(math.radians(angle+180))*20)))
    if positionx < 0:
        positionx = SIZE
    if positionx > SIZE:
        positionx = 0
    if positiony < 0:
        positiony = SIZE
    if positiony > SIZE:
        positiony = 0
    pygame.draw.line(screen, (255, 255, 255), (positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)))
    pygame.draw.line(screen, (255, 255, 255), (positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)))
    pygame.draw.line(screen, (255, 255, 255), (positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx, positiony))
    pygame.draw.line(screen, (255, 255, 255), (positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx, positiony))

if __name__ == "__main__":
    pygame.init()
    myfont = pygame.font.Font("Orbitron-Regular.ttf",20)
    firechannel = pygame.mixer.Channel(0)
    shipchannel = pygame.mixer.Channel(1)
    thrustchannel = pygame.mixer.Channel(2)
    explodechannel = pygame.mixer.Channel(3)
    restart = myfont.render("CLICK ANYWHERE TO RESTART", True, (255, 255, 255))
    scoretext = myfont.render(str(score), True, (255, 255, 255))
    highscoretext = myfont.render(str(highscore), True, (255, 255, 255))
    newhighscoretext = myfont.render("NEW HIGHSC0RE 0F "+str(highscore), True, (255, 255, 255))
    myfont = pygame.font.Font("Orbitron-Regular.ttf",100)
    lose = myfont.render("GAME OVER", True, (255, 255, 255))
    myfont = pygame.font.Font("Orbitron-Regular.ttf",20)
    pygame.display.set_icon(pygame.image.load('asteroid_icon.ico'))
    screen = pygame.display.set_mode((SIZE, SIZE))
    done = False
    clock = pygame.time.Clock()
    for i in range(numberofasteroids):
        randomdecition = random.randint(0, 1)
        if randomdecition == 0:
            randomdecition = random.randint(0, 1)
            asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), random.randint(1, SIZE), randomdecition*SIZE, 0, 0)
        else :
            randomdecition = random.randint(0, 1)
            asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), randomdecition*SIZE, random.randint(1, SIZE), 0, 0)
        asteroids.append(asteroid)
    pygame.display.set_caption("Asteroids by Torin", "Asteroids")
    while not done:
        screen.fill((0, 0, 0))
        if mothership_counter != 0:
            mothership_counter -= 1
        else:
            if not mothership_disperse:
                mothership_bullet_counter -= 1 
                if mothership_bullet_counter == 0:
                    mothership_bullet_counter = random.randint(10, 70)
                    bullet = make_mothership_bullet()
                    if mothership_type == 1:
                        bullet.change_x = math.sin(math.radians(math.degrees(math.asin((positionx-mothership_x)/math.dist((mothership_x, mothership_y), (positionx, positiony))))+random.randint(mothership_offset*-1, mothership_offset)))*7
                        bullet.change_y = math.cos(math.radians(math.degrees(math.acos((positiony-mothership_y)/math.dist((mothership_x, mothership_y), (positionx, positiony))))+random.randint(mothership_offset*-1, mothership_offset)))*7
                    else:
                        randomdecition = random.randint(0, 360)
                        bullet.change_x = math.sin(math.radians(randomdecition))*7
                        bullet.change_y = math.cos(math.radians(randomdecition))*7
                    mothership_bullets.append(bullet) 
            pygame.draw.line(screen, (255, 255, 255), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))
            pygame.draw.line(screen, (255, 255, 255), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))
            mothership_x += mothership_change_x
            mothership_y += mothership_change_y
            if not mothership_on:
                shipchannel.play(Sound("siren.ogg"), loops=-1)
                mothership_on = True
                if score > 40000:
                    mothership_type = 1
            if mothership_x < 0:
                if mothership_disperse:
                    mothership_on = False
                    mothership_counter = random.randint(600, 900)
                    mothership_type = (mothership_counter % 2)+1
                    mothership_x = 0
                    mothership_y = random.randint(0, SIZE)
                    mothership_change_x = random.randint(-250, 250)/100
                    mothership_change_y = random.randint(-250, 250)/100
                    mothership_bullet_counter = random.randint(10, 70)
                    mothership_disperse = False
                    mothership_offset = 57
                    mothership_direction_change_counter = random.randint(60, 120)
                    shipchannel.stop()
                mothership_x = SIZE
            if mothership_x > SIZE:
                if mothership_disperse:
                    mothership_on = False
                    mothership_counter = random.randint(600, 900)
                    mothership_type = (mothership_counter % 2)+1
                    mothership_x = 0
                    mothership_y = random.randint(0, SIZE)
                    mothership_change_x = random.randint(-250, 250)/100
                    mothership_change_y = random.randint(-250, 250)/100
                    mothership_bullet_counter = random.randint(10, 70)
                    mothership_disperse = False
                    mothership_offset = 57
                    mothership_direction_change_counter = random.randint(60, 120)
                    shipchannel.stop()
                mothership_x = 0
            if mothership_y < 0:
                if mothership_disperse:
                    mothership_on = False
                    mothership_counter = random.randint(600, 900)
                    mothership_type = (mothership_counter % 2)+1
                    mothership_x = 0
                    mothership_y = random.randint(0, SIZE)
                    mothership_change_x = random.randint(-250, 250)/100
                    mothership_change_y = random.randint(-250, 250)/100
                    mothership_bullet_counter = random.randint(10, 70)
                    mothership_disperse = False
                    mothership_offset = 57
                    mothership_direction_change_counter = random.randint(60, 120)
                    shipchannel.stop()
                mothership_y = SIZE
            if mothership_y > SIZE:
                if mothership_disperse:
                    mothership_on = False
                    mothership_counter = random.randint(600, 900)
                    mothership_type = (mothership_counter % 2)+1
                    mothership_x = 0
                    mothership_y = random.randint(0, SIZE)
                    mothership_change_x = random.randint(-250, 250)/100
                    mothership_change_y = random.randint(-250, 250)/100
                    mothership_bullet_counter = random.randint(10, 70)
                    mothership_disperse = False
                    mothership_offset = 57
                    mothership_direction_change_counter = random.randint(60, 120)
                    shipchannel.stop()
                mothership_y = 0
            if not mothership_disperse:
                mothership_direction_change_counter -= 1
                if mothership_direction_change_counter == 0:
                    mothership_change_x = random.randint(-250, 250)/100
                    mothership_change_y = random.randint(-250, 250)/100
                    mothership_direction_change_counter = random.randint(60, 120)
        screen.blit(highscoretext, (5, SIZE - 25))
        if explodecounter != 0:
            explodecounter -= 1
        else:
            if dead == True:
                screen.blit(lose, (SIZE/2-351.5, SIZE/2 - 50))
                screen.blit(newhighscoretext, (SIZE/2-(147+(digits(score)*7)), SIZE/2+55))
                screen.blit(restart, (SIZE/2 - 200, SIZE/2 + 80))
            asteroid_number = 0
            asteroid_position_check = 0
            for asteroid in asteroids:
                asteroid_number += 1
                if not(((asteroid.x > (SIZE/2) - 80) and (asteroid.y > (SIZE/2) - 80)) and ((asteroid.x < (SIZE/2) + 80) and (asteroid.y < (SIZE/2) + 80))):
                    asteroid_position_check += 1
            if (explode == True) and (asteroid_position_check == asteroid_number):
                positionx = SIZE/2
                positiony = SIZE/2
                speedx = 0
                speedy = 0
                explode = False
        for i in range(lives):
            pygame.draw.line(screen, (255, 255, 255), (95-(i*15), 50), (90-(i*15), 70))
            pygame.draw.line(screen, (255, 255, 255), (95-(i*15), 50), (100-(i*15), 70))
            pygame.draw.line(screen, (255, 255, 255), (100-(i*15), 70), (95-(i*15), 62))
            pygame.draw.line(screen, (255, 255, 255), (90-(i*15), 70), (95-(i*15), 62))
        scoretext = myfont.render(str(score), True, (255, 255, 255))
        screen.blit(scoretext, ((100-(digits(score)*14)), 27))
        pygame.draw.line(screen, (255, 255, 255), (45, 45), (100, 45))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dead == True:
                    shipchannel.stop()
                    dead = False
                    angle = 0
                    rotateby = 0
                    positionx = SIZE/2
                    positiony = SIZE/2
                    thruston = False
                    speedx = 0
                    speedy = 0
                    bullets = []
                    bulletcreate = False
                    asteroids = []
                    randomdecition = 0
                    explodelines = []
                    explode = False
                    explodecounter = 0
                    asteroid_position_check = 0
                    asteroid_number = 0
                    score = 0
                    lives = random.randint(3, 5)
                    numberofasteroids = 4
                    extralifescounter = 0
                    mothership_bullets = []
                    mothership_bullet_counter = random.randint(10, 70)
                    mothership_disperse = False
                    mothership_offset = 57
                    mothership_direction_change_counter = random.randint(60, 120)
                    MOTHERSHIP_SIZE = 0.75
                    mothership_counter = random.randint(600, 900)
                    mothership_type = (mothership_counter % 2)+1
                    mothership_x = 0
                    mothership_y = random.randint(0, SIZE)
                    mothership_change_x = random.randint(-250, 250)/100
                    mothership_change_y = random.randint(-250, 250)/100
                    mothership_on = False
                    for i in range(numberofasteroids):
                        randomdecition = random.randint(0, 1)
                        if randomdecition == 0:
                            randomdecition = random.randint(0, 1)
                            asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), random.randint(1, SIZE), randomdecition*SIZE, 0, 0)
                        else :
                            randomdecition = random.randint(0, 1)
                            asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), randomdecition*SIZE, random.randint(1, SIZE), 0, 0)
                        asteroids.append(asteroid)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_o:
                    rotateby += 4
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_p:
                    rotateby -= 4
                elif event.key == pygame.K_UP or event.key == pygame.K_q:
                    thruston = True
                    if (not explode) and (not dead):
                        thrustchannel.play(Sound("thrust.ogg"), loops=-1)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_a:
                    if (not explode) and (not dead):
                        bullet = make_bullet() 
                        bullets.append(bullet)
                        firechannel.play(Sound("fire_sound_torin.ogg"))
                elif event.key == pygame.K_h:
                    positionx = random.randint(0, SIZE)
                    positiony = random.randint(0, SIZE)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_o:
                    rotateby -= 4
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_p:
                    rotateby += 4
                elif event.key == pygame.K_UP or event.key == pygame.K_q:
                    thruston = False
                    thrustchannel.stop()
        bulletprevious = bullets
        for explotion in explodelines:
            explotion.x += explotion.change_x
            explotion.y += explotion.change_y
            explotion.angle += explotion.change_angle
            explotion.counter -= 1
            if explotion.counter == 0:
                explodelines.remove(explotion)
            pygame.draw.line(screen, (255, 255, 255), (explotion.x, explotion.y), ((math.sin(math.radians(explotion.angle))*explotion.length)+explotion.x, (math.cos(math.radians(explotion.angle))*explotion.length)+explotion.y))
        for bullet in bullets:
            bullet.xprev = bullet.x - bullet.change_x*2
            bullet.yprev = bullet.y - bullet.change_y*2
            bullet.x += bullet.change_x
            bullet.y += bullet.change_y
            screen.set_at((round(bullet.x), round(bullet.y)), (255, 255, 255))
            if bullet.y > SIZE or bullet.y < 0 or bullet.x > SIZE or bullet.x < 0:
                bullets.remove(bullet)
            elif mothership_on:
                if ((None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE))))):
                    explotion = make_explotion(mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y, random.randint(-300, 300)/100, random.randint(-300, 300)/100, 90, 30)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y, random.randint(-300, 300)/100, random.randint(-300, 300)/100, 135, 10.60660172)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y, random.randint(-300, 300)/100, random.randint(-300, 300)/100, 45, 10.60660172)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y, random.randint(-300, 300)/100, random.randint(-300, 300)/100, 225, 10.60660172)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y, random.randint(-300, 300)/100, random.randint(-300, 300)/100, 315, 10.60660172)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x-(7.5*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7.5*mothership_type*MOTHERSHIP_SIZE), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 90, 15)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x-(7.5*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7.5*mothership_type*MOTHERSHIP_SIZE), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 90, 15)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 180, 6.5)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 180, 6.5)
                    explodelines.append(explotion)
                    explotion = make_explotion(mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 90, 14)
                    explodelines.append(explotion)
                    shipchannel.stop()
                    explodechannel.play(Sound("explode_sound_torinv2.ogg"))
                    bullets.remove(bullet)
                    mothership_on = False
                    mothership_direction_change_counter = random.randint(60, 120)
                    mothership_counter = random.randint(600, 900)
                    mothership_type = (mothership_counter % 2)+1
                    mothership_x = 0
                    mothership_y = random.randint(0, SIZE)
                    mothership_change_x = random.randint(-250, 250)/100
                    mothership_change_y = random.randint(-250, 250)/100
                    score += int(200+(1600/mothership_type))
                    if mothership_offset > 5:
                        mothership_offset -= 5
        for asteroid in asteroids:
            asteroid.angle += asteroid.anglechange
            asteroid.x += asteroid.changex
            asteroid.y += asteroid.changey
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))
            pygame.draw.line(screen, (255, 255, 255), (((math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y), (((math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))
            if asteroid.x < 0:
                asteroid.x = SIZE
            if asteroid.x > SIZE:
                asteroid.x = 0
            if asteroid.y < 0:
                asteroid.y = SIZE
            if asteroid.y > SIZE:
                asteroid.y = 0
            if explode == False and dead == False and math.dist((positionx, positiony), (asteroid.x, asteroid.y)) < (asteroid.Size/4*asteroid_size*20)+20:
                if ((None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), ((asteroid.x+(math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y)))):
                        lives -= 1
                        explode = True
                        explodecounter = 120
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 20+angle, 20)
                        explodelines.append(explotion)
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 20+angle, 20)
                        explodelines.append(explotion)
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -20+angle, 20)
                        explodelines.append(explotion)
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -20+angle, 20)
                        explodelines.append(explotion)
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 10+angle, 39.39231012)
                        explodelines.append(explotion)
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 10+angle, 39.39231012)
                        explodelines.append(explotion)
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -10+angle, 39.39231012)
                        explodelines.append(explotion)
                        explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -10+angle, 39.39231012)
                        explodelines.append(explotion)
                        explodechannel.play(Sound("explode_sound_torinv2.ogg"))
                        if lives == 0:
                            newhighscoretext = myfont.render("G00D. YOUR SC0RE IS "+str(score), True, (255, 255, 255))
                            if score > highscore:
                                with open('asteroids_high_score.txt', 'w') as f:
                                    f.write(str(score))
                                    highscore = score
                                    highscoretext = myfont.render(str(highscore), True, (255, 255, 255))
                                    newhighscoretext = myfont.render("NEW HIGHSC0RE 0F "+str(highscore), True, (255, 255, 255))
                            f.close()
                            asteroid_number = 4
                            dead = True
                            explodecounter = 200
            if explode == False and dead == False:
                if ((None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(15*mothership_type*MOTHERSHIP_SIZE), mothership_y), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(8*mothership_type*MOTHERSHIP_SIZE), mothership_y+(7*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(7*mothership_type*MOTHERSHIP_SIZE)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)))) or 
                    (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (mothership_x+(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE)), (mothership_x-(7*mothership_type*MOTHERSHIP_SIZE), mothership_y-(14*mothership_type*MOTHERSHIP_SIZE))))):
                    lives -= 1
                    explode = True
                    explodecounter = 120
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 20+angle, 20)
                    explodelines.append(explotion)
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 20+angle, 20)
                    explodelines.append(explotion)
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -20+angle, 20)
                    explodelines.append(explotion)
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -20+angle, 20)
                    explodelines.append(explotion)
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 10+angle, 39.39231012)
                    explodelines.append(explotion)
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 10+angle, 39.39231012)
                    explodelines.append(explotion)
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -10+angle, 39.39231012)
                    explodelines.append(explotion)
                    explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -10+angle, 39.39231012)
                    explodelines.append(explotion)
                    explodechannel.play(Sound("explode_sound_torinv2.ogg"))
                    if lives == 0:
                        newhighscoretext = myfont.render("G00D. YOUR SC0RE IS "+str(score), True, (255, 255, 255))
                        if score > highscore:
                            with open('asteroids_high_score.txt', 'w') as f:
                                f.write(str(score))
                                highscore = score
                                highscoretext = myfont.render(str(highscore), True, (255, 255, 255))
                                newhighscoretext = myfont.render("NEW HIGHSC0RE 0F "+str(highscore), True, (255, 255, 255))
                        f.close()
                        asteroid_number = 4
                        dead = True
                        explodecounter = 200
                    else:
                        mothership_disperse = True
                        shipchannel.stop()
            for bullet in bullets:
                if math.dist((bullet.x, bullet.y), (asteroid.x, asteroid.y)) < (asteroid.Size/4*asteroid_size*20)+20:
                    if ((None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(213+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(250+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(255+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(300+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(343+asteroid.angle))*20)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(17+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(24+asteroid.angle))*19)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(65+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(90+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(123+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)+asteroid.y))) or 
                        (None != calculateIntersectPoint((bullet.x, bullet.y), (bullet.xprev, bullet.yprev), ((asteroid.x+(math.sin(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4), (asteroid.y+(math.cos(math.radians(145+asteroid.angle))*15)*asteroid_size*asteroid.Size/4)), (((math.sin(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.x, ((math.cos(math.radians(180+asteroid.angle))*10)*asteroid_size*asteroid.Size/4)+asteroid.y)))):
                            if mothership_offset <= 1:
                                mothership_offset -= 0.3
                            if asteroid.Size == 1:
                                score += 100
                            else:
                                if asteroid.Size == 4:
                                    score += 20
                                else:
                                    score += 50
                                asteroidnew = make_asteroid(asteroid.Size/2, (bullet.change_x/20)+math.sin(math.asin(asteroid.changex-asteroid.takex)-0.5), (bullet.change_y/20)+math.cos(math.acos(asteroid.changey-asteroid.takey)-0.5), asteroid.x, asteroid.y, (bullet.change_x/20), (bullet.change_y/20))
                                asteroids.append(asteroidnew)
                                asteroidnew = make_asteroid(asteroid.Size/2, (bullet.change_x/20)+math.sin(math.asin(asteroid.changex-asteroid.takex)+0.5), (bullet.change_y/20)+math.cos(math.acos(asteroid.changey-asteroid.takey)+0.5), asteroid.x, asteroid.y, (bullet.change_x/20), (bullet.change_y/20))
                                asteroids.append(asteroidnew)
                            asteroids.remove(asteroid)
                            bullets.remove(bullet)
                            if score//10000>extralifescounter:
                                lives+=1
                                extralifescounter+=1
                            if score >= 99990:
                                dead = True
                            break
        for bullet in mothership_bullets:
            bullet.xprev = bullet.x - bullet.change_x*2
            bullet.yprev = bullet.y - bullet.change_y*2
            bullet.x += bullet.change_x
            bullet.y += bullet.change_y
            pygame.draw.line(screen, (255, 255, 255), (bullet.x, bullet.y), (bullet.xprev, bullet.yprev), width=1)
            if bullet.y > SIZE or bullet.y < 0 or bullet.x > SIZE or bullet.x < 0:
                mothership_bullets.remove(bullet)
            if ((None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (bullet.x, bullet.y), (bullet.xprev, bullet.yprev))) or 
                (None != calculateIntersectPoint((positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20)), (positionx + (math.sin(math.radians(angle))*20), positiony + (math.cos(math.radians(angle))*20)), (bullet.x, bullet.y), (bullet.xprev, bullet.yprev)))) and explode == False:
                lives -= 1
                explode = True
                explodecounter = 120
                explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 20+angle, 20)
                explodelines.append(explotion)
                explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 20+angle, 20)
                explodelines.append(explotion)
                explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -20+angle, 20)
                explodelines.append(explotion)
                explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -20+angle, 20)
                explodelines.append(explotion)
                explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 10+angle, 39.39231012)
                explodelines.append(explotion)
                explotion = make_explotion(positionx + (math.sin(math.radians(angle-160))*20), positiony + (math.cos(math.radians(angle-160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, 10+angle, 39.39231012)
                explodelines.append(explotion)
                explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -10+angle, 39.39231012)
                explodelines.append(explotion)
                explotion = make_explotion(positionx + (math.sin(math.radians(angle+160))*20), positiony + (math.cos(math.radians(angle+160))*20), random.randint(-300, 300)/100, random.randint(-300, 300)/100, -10+angle, 39.39231012)
                explodelines.append(explotion)
                explodechannel.play(Sound("explode_sound_torinv2.ogg"))
                if lives == 0:
                    newhighscoretext = myfont.render("G00D. YOUR SC0RE IS "+str(score), True, (255, 255, 255))
                    if score > highscore:
                        with open('asteroids_high_score.txt', 'w') as f:
                            f.write(str(score))
                            highscore = score
                            highscoretext = myfont.render(str(highscore), True, (255, 255, 255))
                            newhighscoretext = myfont.render("NEW HIGHSC0RE 0F "+str(highscore), True, (255, 255, 255))
                    f.close()
                    asteroid_number = 4
                    dead = True
                    explodecounter = 200
                else:
                    mothership_disperse = True
                    shipchannel.stop()
        if angle < 0:
            angle  = angle + 360
        if angle > 359:
            angle  = angle - 360
        if explode == False and dead == False:
            drawship()
        pygame.display.flip()
        if asteroids == [] and not mothership_on:
            numberofasteroids += 2
            for i in range(numberofasteroids):
                randomdecition = random.randint(0, 1)
                if randomdecition == 0:
                    randomdecition = random.randint(0, 1)
                    asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), random.randint(1, SIZE), randomdecition*SIZE, 0, 0)
                else:
                    randomdecition = random.randint(0, 1)
                    asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), randomdecition*SIZE, random.randint(1, SIZE), 0, 0)
                while (((asteroid.x > positionx - 80) and (asteroid.y > positiony - 80)) and ((asteroid.x < positionx + 80) and (asteroid.y < positiony + 80))):
                    randomdecition = random.randint(0, 1)
                    if randomdecition == 0:
                        randomdecition = random.randint(0, 1)
                        asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), random.randint(1, SIZE), randomdecition*SIZE, 0, 0)
                    else :
                        randomdecition = random.randint(0, 1)
                        asteroid = make_asteroid(4, (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), (random.randint(20, 100)/100)*(1-(random.randint(0, 1)*2)), randomdecition*SIZE, random.randint(1, SIZE), 0, 0)
                asteroids.append(asteroid)
        clock.tick(GAME__SPEED)
    pygame.quit()