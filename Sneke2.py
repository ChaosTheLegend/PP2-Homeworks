#This is updated version of Snake, it plays just like a regular snake
#This version has some hard to grasp scripts like collision detection. Please only copy this code if you understand how it works
import pygame
import colorsys
import random

def sign(x):
    if x > 0:
        return 1
    elif x< 0:
        return -1
    elif x == 0:
        return 0


def intersect(colbox1,colbox2):
    if (colbox2[0] <= colbox1[0]+colbox1[2] and colbox2[1] <= colbox1[1]+colbox1[3]) and (colbox2[0]+colbox2[2] >= colbox1[0] and colbox2[1]+colbox2[3] >= colbox1[1]):
        return True
    else:
        return False  

screen = pygame.display.set_mode((800, 600))
rectsize = 16
speed = 5
stop = False

class apple:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.c = 0.01
    def draw(self):
        col = colorsys.hsv_to_rgb(self.c, 1.0, 1.0)
        pygame.draw.circle(screen, (col[0]*255,col[1]*255,col[2]*255), (self.x+8,self.y+8), 8, 0)
        
        #pygame.draw.rect(screen, (255,255,255), (self.x,self.y,rectsize,rectsize), 1)
        self.c+= 0.02
        self.c%= 1.0

class element:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.dx = speed
        self.dy = 0
        
        self.elements = []
        self.pos = [250,250]
        self.elements.append(element(self.pos[0],self.pos[1]))
        self.crashed = False
        self.colbox = (self.pos[0],self.pos[1],0,0)
    def add_element(self):
        self.move()
        self.elements.append(element(0,0))
        

    def draw(self):
        
        l = 0.0
        for i in self.elements:
            col = colorsys.hsv_to_rgb(l, 1.0, 1.0)
            pygame.draw.rect(screen, ((1-col[0])*255,(1-col[1])*255,(1-col[2])*255), (i.x-1,i.y-1,rectsize+2,rectsize+2), 0)
            l+=0.01
            l%=1
        l = 0.0
        for i in self.elements:
            col = colorsys.hsv_to_rgb(l, 1.0, 1.0)
            pygame.draw.rect(screen, (col[0]*255,col[1]*255,col[2]*255), (i.x,i.y,rectsize,rectsize), 0)
            #pygame.draw.rect(screen, (255,255,255), (i.x,i.y,rectsize,rectsize), 1)
            l+=0.01
            l%=1
        #pygame.draw.rect(screen, (120,0,0), self.colbox, 0)
            
    def deleteelem(self):
        if len(self.elements) > 0:
            self.elements = self.elements[0:len(self.elements)-2]
            
    def move(self):
        
        if(self.crashed):
            return
        
        if(self.dx > 0):
            self.colbox = (self.pos[0]+self.dx+rectsize,self.pos[1]+self.dy,1,rectsize)    
        elif(self.dx < 0):
            self.colbox = (self.pos[0]+self.dx,self.pos[1]+self.dy,1,rectsize)    
        elif(self.dy < 0):
            self.colbox = (self.pos[0]+self.dx,self.pos[1]+self.dy,rectsize,1)    
        elif(self.dy > 0):
            self.colbox = (self.pos[0]+self.dx,self.pos[1]+self.dy+rectsize,rectsize,1)    
        

        for k in range(len(self.elements)-1,0,-1):
            self.elements[k].x = self.elements[k-1].x
            self.elements[k].y = self.elements[k-1].y
            if intersect(self.colbox, (self.elements[k].x, self.elements[k].y, rectsize-2, rectsize-2)):
                self.crashed = True

        self.elements[0].x += self.dx
        self.elements[0].y += self.dy
        
        self.pos[0] = self.elements[0].x
        self.pos[1] = self.elements[0].y

        if(self.elements[0].y < 0):
            self.elements[0].y = 600
        if(self.elements[0].y > 600):
            self.elements[0].y = 0
        if(self.elements[0].x < 0):
            self.elements[0].x = 800
        if(self.elements[0].x > 800):
            self.elements[0].x = 0
                  
pygame.init()
play = True

ap = apple(random.randint(50,750),random.randint(50,450)) 

background = pygame.Surface(screen.get_size())
background.fill((255,255,255))  
screen.blit(background, (0,0)) 

snek = Snake()
for i in range(5):
    snek.add_element()

FPS = 60
score = 0
klok = pygame.time.Clock()
playtime = 0

while play:
    milliseconds = klok.tick(FPS) # do not go faster than this framerate
    playtime += milliseconds / 1000.0
    for event in pygame.event.get(): # this empties the event queue. 
        if event.type == pygame.QUIT: 
            play = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if(snek.dy != -speed):
                    snek.dx = 0
                    snek.dy = speed
            if event.key == pygame.K_UP:
                if(snek.dy != speed):
                    snek.dx = 0
                    snek.dy = -speed
            if event.key == pygame.K_LEFT:
                if(snek.dx != speed):
                    snek.dx = -speed
                    snek.dy = 0
            if event.key == pygame.K_RIGHT:
                if(snek.dx != -speed):
                    snek.dx = speed
                    snek.dy = 0
            
    if(abs(snek.pos[0] - ap.x) <= rectsize and abs(snek.pos[1] - ap.y) <= rectsize):
            snek.add_element() 
            #print('apple')
            ap = apple(random.randint(0,800),random.randint(0,600)) 
    if(len(snek.elements) == 0):
        play = False

    if(snek.crashed):
        FPS = (len(snek.elements)/score)*58+2
        snek.deleteelem()
    else:
        score = len(snek.elements)
    #print(snek.pos, ap.x, ap.y)
    
    snek.move()
    screen.fill((0,0,0))
    snek.draw()
    ap.draw()
    #pygame.draw.line(screen, (255,255,255), snek.pos, (ap.x,ap.y), 1)
    
    pygame.display.flip()
            
