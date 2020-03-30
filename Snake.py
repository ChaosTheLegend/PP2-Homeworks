import pygame
import colorsys

screen = pygame.display.set_mode((800, 600))
rectsize = 15
speed = 5

class element:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.size = 1
        self.dx = speed
        self.dy = 0
        
        self.elements = []
        self.pos = [250,250]
        self.elements.append(element(self.pos[0],self.pos[1]))
        
    def add_element(self):
        self.size+=1
        self.move()
        self.elements.append(element(0,0))

    def draw(self):
        l = 0.0
        for i in self.elements:
            col = colorsys.hsv_to_rgb(l, 1.0, 1.0)
            pygame.draw.rect(screen, (col[0]*255,col[1]*255,col[2]*255), (i.x,i.y,rectsize,rectsize), 0)
            l+=0.01
            l%=1

    def move(self):
        for k in range(len(self.elements)-1,0,-1):
            self.elements[k].x = self.elements[k-1].x
            self.elements[k].y = self.elements[k-1].y

        self.elements[0].x += self.dx
        self.elements[0].y += self.dy
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

background = pygame.Surface(screen.get_size())
background.fill((255,255,255))  
screen.blit(background, (0,0)) 

snek = Snake()

FPS = 60

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
            if event.key == pygame.K_z:
                snek.add_element()        
    snek.move()
    screen.fill((0,0,0))
    snek.draw()
    pygame.display.flip()
            
