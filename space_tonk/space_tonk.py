import pygame
import random
import colorsys
from enum import Enum
from pathlib import Path
import os
import math

pygame.init()
screen = pygame.display.set_mode((400,600))
speed = 5
imgdir = Path(os.getcwd())
#imgdir = os.path.join(imgdir,Path("space_tonk"))


tonkimg = pygame.image.load(os.path.join(imgdir,Path("spacetonk.png")))
cosmosimg = pygame.image.load(os.path.join(imgdir,Path("cosmos.png")))
bulletimg = pygame.image.load(os.path.join(imgdir,Path("bullet.png")))
enemyimg = pygame.image.load(os.path.join(imgdir,Path("enemy.png")))
bossimg = pygame.image.load(os.path.join(imgdir,Path("boss.png")))
boss2img = pygame.image.load(os.path.join(imgdir,Path("boss2.png")))
boss3img = pygame.image.load(os.path.join(imgdir,Path("boss3.png")))

bossbulimg = pygame.image.load(os.path.join(imgdir,Path("bossbullet.png")))

bullets = []
enemies = []
bossbullets = []
wave = 1
score = 0

def intersect(colbox1,colbox2):
    if (colbox2[0] <= colbox1[0]+colbox1[2] and colbox2[1] <= colbox1[1]+colbox1[3]) and (colbox2[0]+colbox2[2] >= colbox1[0] and colbox2[1]+colbox2[3] >= colbox1[1]):
        return True
    else:
        return False  

def drawhealthbar(x,y,w,h,value,maxval,fillbg):
    col = colorsys.hsv_to_rgb(((value/maxval)*128)/360, 1.0, 1.0) 
    if(fillbg):
        pygame.draw.rect(screen, (180,180,180), (x-1,y-1,w+2,h+2), 0)
    pygame.draw.rect(screen, (col[0]*255,col[1]*255,col[2]*255), (x,y,int(w*(value/maxval)),h), 0)

class bossbull:
    def __init__(self,x,y,direction,spd):
        self.speed = spd
        self.dx = spd*math.cos(math.radians(direction))
        self.dy = spd*math.sin(math.radians(direction))
        self.x = x
        self.y = y
        self.bounds = (self.x,self.y,30,30)

    def move(self):
        self.x += self.dx*ticks
        self.y += self.dy*ticks
        self.bounds = (self.x,self.y,30,30)

    def draw(self):
        screen.blit(bossbulimg, (int(self.x),int(self.y)))


class boss:
    
    def death(self):
        self.deathrot+=25.2
        bb = bossbull(self.x+150,self.y+210,self.deathrot,6)
        bossbullets.append(bb)
            


    def pattern1(self):
        for i in range(5):
            bb = bossbull(self.x+100,self.y+205,40+i*24,5)
            bossbullets.append(bb)
            bb2 = bossbull(self.x+205,self.y+208,40+i*24,5)
            bossbullets.append(bb2)
    
    def pattern2(self):
        for i in range(4):
            bb = bossbull(self.x+100,self.y+205,45+i*30,5)
            bossbullets.append(bb)
            bb2 = bossbull(self.x+205,self.y+208,45+i*30,5)
            bossbullets.append(bb2)

    def pattern3(self):
        for i in range(3):
            bb = bossbull(self.x+100,self.y+205,53+i*40,5)
            bossbullets.append(bb)
            bb2 = bossbull(self.x+205,self.y+208,53+i*40,5)
            bossbullets.append(bb2)

    def pattern4(self):
        for i in range(7):
            bb = bossbull(self.x+100,self.y+205,30+i*20,5)
            bossbullets.append(bb)
            bb2 = bossbull(self.x+205,self.y+208,30+i*20,5)
            bossbullets.append(bb2)

    def pattern5(self):
        for i in range(24):
            bb = bossbull(self.x+150,self.y+210,i*15,5)
            bossbullets.append(bb)
            

    def shoot(self,time):
        self.timer+=time
        if(self.stage == 3):
            self.deathtimer += time
            if(self.timer >= 19):
                self.timer = 0
                self.death()
            if(self.deathtimer >= 4000):
                self.stage = 4
                self.pattern5()
                self.dead = 1
                

        elif(self.timer >= self.delay*1000):
            self.timer = 0
            r = random.randint(0,1+self.stage)
            if(r == 0):
                self.pattern3()
            if(r == 1):
                self.pattern2()
            if(r == 2):
                self.pattern1()
            if(r == 3):
                self.pattern4()


    def __init__(self):
        self.deathrot = 0
        self.x = 50
        self.y = -450
        self.dy = 0
        self.bounds = [(self.x+95,int(self.y)+370,120,50),(self.x+50,int(self.y),200,380),(self.x,int(self.y)+100,300,184)]
        self.health = 100
        self.stage = -1
        self.delay = 1.5
        self.timer = 0
        self.deathtimer = 0
        self.dead = 0
        self.active = False
        self.img = bossimg

    def move(self):
        self.y += self.dy*ticks
        self.bounds = [(self.x+95,int(self.y)+370,120,50),(self.x+50,int(self.y),200,380),(self.x,int(self.y)+100,300,184)]
        

    def draw(self):
        screen.blit(self.img, (int(self.x),int(self.y)))
        drawhealthbar(0,0,400,20,self.health,100,False)
        font = pygame.font.Font('freesansbold.ttf', 18) 
        text = font.render('Boss Health', True, (255,255,255))
        textRect = text.get_rect() 
        textRect.center = (200, 10)
        screen.blit(text, textRect)
        #for hb in self.bounds:
            #pygame.draw.rect(screen, (255,0,0), hb, 1)


    def hit(self):
        if(self.health > 0):
            self.health-=1
        else:
            self.stage = 3
            self.delay = 1000000000000000000000000000000000000
            return

        if(self.health < 50):
            self.img = boss2img
            self.stage = 1
            self.delay = 1.2
        if(self.health < 20):
            self.img = boss3img
            self.stage = 2
            self.delay = 0.8
        
            
        

class enemy:
    def __init__(self):
        self.x = 32
        self.y = -32
        self.dx = -3
        self.dy = 3
        self.bounds = (self.x,self.y,30,30)
        self.lastflip = 0
        self.pattern = 0
        
    def draw(self):
        screen.blit(enemyimg, (int(self.x),int(self.y)))

    def move(self):
        if(self.pattern == 0):
            self.x += self.dx*ticks
            if((self.x > 400-30 and self.dx > 0) or (self.x < 0 and self.dx < 0)):
                self.pattern = 1
                self.lastflip = self.y
        if(self.pattern == 1):
            self.y += self.dy*ticks
            if(self.y > self.lastflip+40):
                self.pattern = 0
                self.dx*= -1
        self.bounds = (self.x,self.y,30,30)
        

        
class bullet:
    def __init__(self, x):
        self.x = x
        self.y = 550
        self.dy = -10
        self.health = 3
        self.bounds = (self.x,self.y,8,16)
    def move(self):
        self.y += self.dy*ticks
        self.bounds = (self.x,self.y,8,16)
        
    def draw(self):
        screen.blit(bulletimg, (int(self.x),int(self.y)))


class Tonk:
    def __init__(self, x, dx):
        self.x = x
        self.dx = dx
        self.bounds = (self.x,550,32,32)
        self.health = 10
    def draw(self):
        screen.blit(tonkimg, (int(self.x),550))
        drawhealthbar(self.x-10,550+35,32+20,10,self.health,10,True)

    def move(self):
        self.x += self.dx*ticks*speed
        self.bounds = (self.x,550,32,32)

    def shoot(self):
        bl = bullet(self.x+12)
        bullets.append(bl)

bs = boss()
secconds = 0
play = True
tk = Tonk(200,0)
klok = pygame.time.Clock()
FPS = 60
time = 0
while play:
    mills = klok.tick(FPS)
    ticks = mills/20.0
    if(score < 30):
        time += mills
    elif len(enemies) == 0:
        wave = 2
        bs.active = 1
    if(time >= 0.3*1000):
        time = 0
        enem = enemy()
        enemies.append(enem)

    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
             play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tk.dx = -1
            if event.key == pygame.K_RIGHT:
                tk.dx = 1
            if(event.key == pygame.K_SPACE):
                tk.shoot()
            if event.key == pygame.K_ESCAPE:
                play =False    
        if event.type == pygame.KEYUP:
            k = event.key
            if k == pygame.K_RIGHT or k == pygame.K_LEFT:
                tk.dx = 0
    screen.blit(cosmosimg, (0,0))        
    for b in bullets:
        b.move()
        b.draw()
        if(b.y < 0):
            bullets.remove(b)
        if(bs.dead == 0 and bs.active and bs.stage != -1):
            for hb in bs.bounds :
                if(intersect(hb,b.bounds)):
                    bs.hit()
                    bullets.remove(b)

    for e in enemies:
        e.move()
        e.draw()

    if(bs.dead == 0 and bs.active):
        bs.draw()
        if(bs.stage == -1):
            bs.dy = 2
            bs.move()
            if(bs.y >= 30):
                bs.stage = 0
                bs.dy = 0
        else:
            bs.shoot(mills)
        

    for bb in bossbullets:
        bb.move()
        bb.draw()
        if(intersect(bb.bounds,tk.bounds)):
            bossbullets.remove(bb)
            tk.health-=1
        if bb.y > 620 or bb.y < -60 or bb.x > 440 or bb.x < -40 :
            bossbullets.remove(bb)

    if(len(enemies) > 0 and len(bullets) > 0):
        for e in enemies:
            for b in bullets:
                if(intersect(e.bounds,b.bounds)):
                    bullets.remove(b)
                    enemies.remove(e)
                    score+=1

    if(tk.health == 0):
        play = False
        break
    
    if(bs.dead):
        font1 = pygame.font.Font('freesansbold.ttf', 50) 
        text1 = font1.render('You Win!', True, (255,255,255))
        textRect1 = text1.get_rect() 
        textRect1.center = (200, 300)
        screen.blit(text1, textRect1)
        

    tk.move()
    if tk.x < 0:
        tk.x = 0

    if tk.x > 400-32:
        tk.x = 400-32
        
    tk.draw()
    pygame.display.flip()
    
