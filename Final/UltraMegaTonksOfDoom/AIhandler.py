import pygame
import colorsys
import math
import random
import ResourceLoader as rs
import GraphicsHelper as gh

bulletimg = rs.LoadImage('bullet.png')

shotsnd = rs.LoadSound('Shot.ogg')
destroysnd = rs.LoadSound('destroy.ogg')
nickfont = pygame.font.Font('freesansbold.ttf', 14)

speed = 2.5
bulletspeed = 5


def FindNearest(tks,me):
    nearest = ''
    nearestdis = 20000000000000
    for tk in tks:
        if(tk != me.nick):
            dis = (me.x-tks[tk].x)**2+(me.y-tks[tk].y)**2
            if(dis < nearestdis):
                nearest = tks[tk]
                nearestdis = dis
    return nearest

def getSqrDistance(pos1,pos2):
    return (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2

def FindNearestBul(buls,me):
    nearest = ''
    nearestdis = 20000000000000
    for bl in buls:
        if(bl.owner != me.nick):
            dis = (me.x-bl.x)**2+(me.y-bl.y)**2
            if(dis < nearestdis):
                nearest = bl
                nearestdis = dis
    return nearest

class AItonk:
    def __init__(self,x,y,col,nick,score,displaynick,agorrad,avoidrad,img):
        #coordinates
        self.x = x
        self.y = y
        
        self.score = score
        self.agorrad = agorrad
        self.avoidrad = avoidrad
        #velosity
        self.dx = 0
        self.dy = 0
        self.dir = 1
        self.powerh = 0

        #display        
        self.col = col
        self.nick = nick
        self.shoottm = 1000
        self.delay = 1000
        
        #extras
        self.health = 3
        self.surf = pygame.Surface((32, 32))
        self.displaynick = displaynick
        self.img = img

        #AI info
        self.state = 'Idle'
        self.target = ''
        self.nearestbul = ''

        self.tonks = {}
        self.bullets = []

    def draw(self,screen):
        intx = int(self.x)
        inty = int(self.y)
        drawsurf = pygame.Surface((32, 32))
        
        alphacol = (2,2,2)
        drawsurf.fill(alphacol)
        
        #drawing tank sprite
        self.surf.blit(self.img,(0,0))
        #transparancy
        self.surf.set_colorkey(alphacol)
        #tank rotation
        drawsurf = pygame.transform.rotate(self.surf, -90*self.dir)
        #drawing tank
        screen.blit(drawsurf,(intx,inty))
        #healthbar
        gh.DrawHealthbar(intx-2,inty+36,36,8,self.health,3,0,True,screen)
        gh.DrawHealthbar(intx-10,inty,8,32,self.delay-self.shoottm,self.delay,3,True,screen,(255,255,0))    
        
        #nick
        gh.DrawText(self.displaynick,nickfont,(255,255,255),(int(self.x+16), int(self.y-22+12)),screen)
        
        #AI Draw:
        for tk in self.tonks:
            pygame.draw.line(screen, (0,0,255), (self.x,self.y), (self.tonks[tk].x,self.tonks[tk].y))

        for bl in self.bullets:
            pygame.draw.line(screen, (255,0,0), (self.x,self.y), (bl.x,bl.y))

        if(self.target != ''):
            pygame.draw.line(screen, (0,255,0), (self.x,self.y), (self.target.x,self.target.y))

        if(self.nearestbul != ''):
            pygame.draw.line(screen, (255,255,0), (self.x,self.y), (self.nearestbul.x,self.nearestbul.y))

        pygame.draw.circle(screen, (255,255,0), (intx+16,inty+16), self.agorrad, 1)
        pygame.draw.circle(screen, (255,0,0), (intx+16,inty+16), self.avoidrad, 1)



    def getAction(self):
        if(self.state == 'FollowX'):
            if(self.target.x > self.x):
                if(self.dir != 1):
                    return 'TrunRight'
            elif(self.dir != 3):
                    return 'TrunLeft'

        if(self.state == 'FollowY'):
            if(self.target.y > self.y):
                if(self.dir != 2):
                    return 'TrunDown'
            elif(self.dir != 0):
                    return 'TrunUp'
        
        if(self.state == 'AimY'):
            if(self.target.y > self.y):
                if(self.dir != 2):
                    return 'TrunDown'
            elif(self.dir != 0):
                    return 'TrunUp' 

        if(self.state == 'AimX'):
            if(self.target.x > self.x):
                if(self.dir != 1):
                    return 'TrunRight'
            elif(self.dir != 3):
                    return 'TrunLeft'

        if(self.state == 'Fire' and self.shoottm <= 0):
            return 'Fire'
        
        if(self.state == 'FleeX'):
            if(self.x >= self.nearestbul.x):
                if(self.dir != 1):
                    return 'TrunRight'
            elif(self.dir != 3):
                return 'TrunLeft'
            
        if(self.state == 'FleeY'):
            if(self.dir == 1 or self.dir == 3):
                if(self.y >= self.nearestbul.y):
                    if(self.dir != 2):
                        return 'TrunDown'
                elif(self.dir != 0):
                    return 'TrunUp'
            


        return 'None'


    def update(self,tick):
        if(self.shoottm > 0):
            self.shoottm -= tick*20
        if(self.shoottm <0):
            self.shoottm = 0
        #AI
        self.target = FindNearest(self.tonks,self)
        self.nearestbul = FindNearestBul(self.bullets,self)
        if(self.target == ''):
            self.state = 'Idle'
            return

        xdif = self.target.x - self.x 
        ydif = self.target.y - self.y
        if(abs(xdif) > abs(ydif)):
            self.state = 'FollowX'
        if(abs(ydif) > abs(xdif)):
            self.state = 'FollowY'

#        if(abs(xdif) < 100):
#            self.state = 'FollowY'
#        if(abs(ydif) < 100):
#            self.state = 'FollowX'

        if (self.nearestbul!= '' and getSqrDistance((self.x,self.y),(self.nearestbul.x,self.nearestbul.y)) < self.avoidrad**2):    
            if self.nearestbul.dx !=0:
                self.state = 'FleeY'
                
            if self.nearestbul.dy !=0:
                self.state = 'FleeX'
            return

        if(not getSqrDistance((self.x,self.y),(self.target.x,self.target.y)) < self.agorrad**2):
            return

        if(abs(xdif) < abs(ydif)):
            self.state = 'FollowX'
        if(abs(ydif) < abs(xdif)):
            self.state = 'FollowY'
            
        if(abs(xdif) < 16):
            if(self.dir == 1 or self.dir == 3):
                self.state = 'AimY'
            else:
                self.state = 'Fire'
        if(abs(ydif) < 16):
            if(self.dir == 0 or self.dir == 2):
                self.state = 'AimX'
            else:
                self.state = 'Fire'
        
        
        

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