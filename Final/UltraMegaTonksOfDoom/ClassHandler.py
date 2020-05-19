import pygame
import colorsys
import math
import random
import ResourceLoader as rs
import GraphicsHelper as gh

tonkimg = rs.LoadImage('tonk.png')
bulletimg = rs.LoadImage('bullet.png')

shotsnd = rs.LoadSound('Shot.ogg')
destroysnd = rs.LoadSound('destroy.ogg')
nickfont = pygame.font.Font('freesansbold.ttf', 14)

speed = 2.5
bulletspeed = 5

class powerup:
    def __init__(self,x,y,action):
        self.x = x
        self.y = y
        self.bounds = (self.x-8,self.y-8,16,16) #bounds for checking collision
        self.h = 0
        self.type = action
        
    def draw(self,screen):
        self.h %= 360
        #draw lightning:
        points = []
        col = ()
        if(self.type == 1):
            points = [(self.x-7,self.y+1),(self.x-3,self.y-9),(self.x+6,self.y-9),(self.x+2,self.y-3),(self.x+7,self.y-3),(self.x-2,self.y+9),(self.x,self.y+1)]
            col = (255,128+math.sin(math.radians(self.h))*50,0)
            self.h += 2
        if(self.type == 2):
            points = [(self.x-2,self.y+8),(self.x+2,self.y+8),(self.x+2,self.y+2),(self.x+8,self.y+2),(self.x+8,self.y-2),(self.x+2,self.y-2),(self.x+2,self.y-8),(self.x-2,self.y-8),
            (self.x-2,self.y-2),(self.x-8,self.y-2),(self.x-8,self.y+2),(self.x-2,self.y+2)]
            col = (90+math.sin(math.radians(self.h))*90,255,90+math.sin(math.radians(self.h))*90)
            self.h += 0.5
        if(self.type == 3):
            points = [(self.x-2,self.y-2),(self.x-2,self.y-8),(self.x+8,self.y-8),(self.x+8,self.y-6),(self.x+2,self.y-6),(self.x+2,self.y-2),(self.x+8,self.y-2),
            (self.x+8,self.y+8),(self.x+6,self.y+8),(self.x+6,self.y+2),(self.x+2,self.y+2),(self.x+2,self.y+8),(self.x-8,self.y+8),(self.x-8,self.y+6),
            (self.x-2,self.y+6),(self.x-2,self.y+2),(self.x-8,self.y+2),(self.x-8,self.y-8),(self.x-6,self.y-8),(self.x-6,self.y-2)]
            col = (200+math.sin(math.radians(self.h))*50,0,0)
            self.h += 1
        
        
        pygame.draw.polygon(screen, col, points)
        
class block:
    def __init__(self,x,y,img,health):
        self.hp = health
        self.sprite = img
        self.bounds = (x,y,32,32) #bounds for checking collision
    def draw(self,screen):
        screen.blit(self.sprite,(int(self.bounds[0]),int(self.bounds[1])))

class bullet:
    def __init__(self,x,y,dx,dy,owner):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bounds = (self.x,self.y,4,4) #bounds for checking collision
        self.owner = owner
        self.type = 0
        
    def draw(self,screen):
        if self.type == 0:
            screen.blit(bulletimg,(int(self.x),int(self.y)))
        if self.type == 1:
            points = [(self.x-2,self.y-2),(self.x-2,self.y-8),(self.x+8,self.y-8),(self.x+8,self.y-6),(self.x+2,self.y-6),(self.x+2,self.y-2),(self.x+8,self.y-2),
            (self.x+8,self.y+8),(self.x+6,self.y+8),(self.x+6,self.y+2),(self.x+2,self.y+2),(self.x+2,self.y+8),(self.x-8,self.y+8),(self.x-8,self.y+6),
            (self.x-2,self.y+6),(self.x-2,self.y+2),(self.x-8,self.y+2),(self.x-8,self.y-8),(self.x-6,self.y-8),(self.x-6,self.y-2)]
            pygame.draw.polygon(screen, (255,0,0), points)
        

    def move(self,tick):
        self.x += self.dx*tick
        self.y += self.dy*tick
        self.bounds = (self.x,self.y,4,4) #bounds update

class mpbullet:
    def __init__(self,x,y,w,h,direction,owner):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = (255,0,0)
        dx = 0
        dy = 0

        if(direction == 1):
            dx = 1
            dy = 0
        elif(direction == 3):
            dx = -1
            dy = 0
        elif(direction== 2):
            dy = 1
            dx = 0
        elif(direction == 0):
            dy = -1
            dx = 0

        self.owner = owner
        self.dx = dx
        self.dy = dy
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.col, (self.x,self.y,self.w,self.h))

    def move(self,tick):
        self.x += self.dx*tick*100
        self.y += self.dy*tick*100
        
        
class tonk:
    def __init__(self,x,y,col,nick,score):
        #coordinates
        self.x = x
        self.y = y
        
        self.score = score
        self.bounds = (x,y,32,32) 
        #velosity
        self.dx = 0
        self.dy = 0
        self.dir = 1
        self.powerh = 0
        self.speed = speed

        #display        
        self.col = col
        self.nick = nick
        self.shoottm = 1000
        self.delay = 1000
        
        self.powertm = 0
        self.hitler = False

        #extras
        self.health = 3
        self.surf = pygame.Surface((32, 32))
        
    def draw(self,screen):
        intx = int(self.x)
        inty = int(self.y)
        drawsurf = pygame.Surface((32, 32))
        
        alphacol = (2,2,2)
        drawsurf.fill(alphacol)
        
        #tank color
        if(self.powertm <= 0):
            pygame.draw.rect(self.surf, self.col, (0,6,32,20), 0)
            pygame.draw.rect(self.surf, self.col, (14,0,4,10), 0)
        else:
            pygame.draw.rect(self.surf, (255,128+math.sin(math.radians(self.powerh))*50,0), (0,0,32,32), 0)
            self.powerh +=2
            self.powerh %= 360

        #drawing tank sprite
        self.surf.blit(tonkimg,(0,0))
        #transparancy
        self.surf.set_colorkey(alphacol)
        #tank rotation
        drawsurf = pygame.transform.rotate(self.surf, -90*self.dir)
        #drawing tank
        screen.blit(drawsurf,(intx,inty))
        #healthbar
        
        gh.DrawHealthbar(intx-2,inty+36,36,8,self.health,3,0,True,screen)
        if(self.delay > 0):
            gh.DrawHealthbar(intx-10,inty,8,32,max(1,self.delay-self.shoottm),self.delay,3,True,screen,(255,255,0))
        if(self.powertm > 0):
            gh.DrawHealthbar(intx-2,inty+36,36,8,self.powertm,5000,0,False,screen,(255,130,0))
            
        
        #nick
        gh.DrawText(self.nick,nickfont,(255,255,255),(int(self.x+16), int(self.y-22+12)),screen)
        
    def shoot(self):
        if(self.shoottm == 0):
            self.shoottm = self.delay
            shotsnd.play()
            bl = ''
            speedmult = (self.speed/speed)
            if(self.dir == 1):
                bl = bullet(self.x+32,self.y+14,bulletspeed*speedmult,0,self.nick)
            elif(self.dir == 3):
                bl = bullet(self.x-4,self.y+14,-bulletspeed*speedmult,0,self.nick)        
            elif(self.dir == 2):
                bl = bullet(self.x+14,self.y+32,0,bulletspeed*speedmult,self.nick)
            elif(self.dir == 0):
                bl = bullet(self.x+14,self.y-4,0,-bulletspeed*speedmult,self.nick)
            if(self.hitler):
                bl.type = 1
            return bl        
        return None

    def update(self,tick):
        if(self.shoottm > 0):
            self.shoottm -= tick*20
        if(self.shoottm <0):
            self.shoottm = 0

        if(self.powertm <= 0):
            self.speed = speed
        else:
            self.powertm -= tick*20

    def dirmove(self,tick):
        if(self.dir == 1):
            self.dx = 1
            self.dy = 0
        elif(self.dir == 3):
            self.dx = -1
            self.dy = 0
        elif(self.dir == 2):
            self.dy = 1
            self.dx = 0
        elif(self.dir == 0):
            self.dy = -1
            self.dx = 0

        self.x += self.dx*tick*50
        self.y += self.dy*tick*50


    def move(self,tick):
        #changing direction
        if(self.dx > 0):
            self.dir = 1
        elif(self.dx < 0):
            self.dir = 3
        elif(self.dy > 0):
            self.dir = 2
        elif(self.dy < 0):
            self.dir = 0
        
        #movement
        self.x += self.dx*tick*self.speed
        self.y += self.dy*tick*self.speed

        #updating bounds
        self.bounds = (self.x,self.y,32,32)