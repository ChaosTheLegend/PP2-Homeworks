import pygame
import colorsys
from pathlib import Path
import os
import math

speed = 5
bulletspeed = 7

pygame.init()
screen = pygame.display.set_mode((800,600))

#image loader:
imgdir = Path(__file__).parent

#imgdir = Path(os.getcwd())
#imgdir = os.path.join(imgdir,Path("SupraTonks"))
print(imgdir)
def LoadImage(name):
    return pygame.image.load(os.path.join(imgdir,Path(name)))

tonkimg = LoadImage('tonk.png')
bulletimg = LoadImage('bullet.png')
nickfont = pygame.font.Font('freesansbold.ttf', 14)
        
#colorgen
def createcol(h):
    col = colorsys.hsv_to_rgb(h/360, 1.0, 1.0) 
    return (col[0]*255,col[1]*255,col[2]*255) 

#healthbars
def drawhealthbar(x,y,w,h,value,maxval,fillbg):
    col = colorsys.hsv_to_rgb(((value/maxval)*128)/360, 1.0, 1.0) 
    if(fillbg):
        pygame.draw.rect(screen, (180,180,180), (x-1,y-1,w+2,h+2), 0)
    pygame.draw.rect(screen, (col[0]*255,col[1]*255,col[2]*255), (x,y,int(w*(value/maxval)),h), 0)

#collison
def intersect(colbox1,colbox2):
     return(colbox2[0] <= colbox1[0]+colbox1[2] and colbox2[1] <= colbox1[1]+colbox1[3]) and (colbox2[0]+colbox2[2] >= colbox1[0] and colbox2[1]+colbox2[3] >= colbox1[1])


class bullet:
    def __init__(self,x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bounds = (self.x,self.y,4,4) #bounds for checking collision
        
    def draw(self):
        screen.blit(bulletimg,(int(self.x),int(self.y)))

    def move(self):
        self.x += self.dx*tick
        self.y += self.dy*tick
        self.bounds = (self.x,self.y,4,4) #bounds update
    
class tonk:
    def __init__(self,x,y,col,nick):
        #coordinates
        self.x = x
        self.y = y
        
        self.bounds = (x,y,32,32) 
        #velosity
        self.dx = 0
        self.dy = 0
        self.dir = 1
        
        #display        
        self.col = col
        self.nick = nick

        #extras
        self.health = 20
        self.surf = pygame.Surface((32, 32))
        
    def draw(self):
        intx = int(self.x)
        inty = int(self.y)
        drawsurf = pygame.Surface((32, 32))
        
        alphacol = (2,2,2)
        drawsurf.fill(alphacol)
        
        #tank color
        pygame.draw.rect(self.surf, self.col, (0,6,32,20), 0)
        pygame.draw.rect(self.surf, self.col, (14,0,4,10), 0)
        #drawing tank sprite
        self.surf.blit(tonkimg,(0,0))
        #tank rotation
        drawsurf = pygame.transform.rotate(self.surf, -90*self.dir)
        #transparancy
        drawsurf.set_colorkey(alphacol)
        #drawing tank
        screen.blit(drawsurf,(intx,inty))
        #healthbar
        drawhealthbar(intx-2,inty+36,36,8,self.health,20,True)
        #nick
        text = nickfont.render(self.nick, True, (255,255,255))
        textRect = text.get_rect() 
        textRect.center = (int(self.x+16), int(self.y-22+12))
        #drawing extras
        screen.blit(text, textRect)
        
    def shoot(self):
        bl = ''
        if(self.dir == 1):
            bl = bullet(self.x+32,self.y+14,bulletspeed,0)
        elif(self.dir == 3):
            bl = bullet(self.x-4,self.y+14,-bulletspeed,0)        
        elif(self.dir == 2):
            bl = bullet(self.x+14,self.y+32,0,bulletspeed)
        elif(self.dir == 4):
            bl = bullet(self.x+14,self.y-4,0,-bulletspeed)
        bullets.append(bl)

    def move(self):
        #changing direction
        if(self.dx > 0):
            self.dir = 1
        elif(self.dx < 0):
            self.dir = 3
        elif(self.dy > 0):
            self.dir = 2
        elif(self.dy < 0):
            self.dir = 4
        #checking collision with other tanks
        nextbounds = (self.x+self.dx*tick,self.y+self.dy*tick,32,32)
        for k in tonks:
            if(tonks[k] != self):
                if(intersect(nextbounds, tonks[k].bounds)):
                    return
        
        #movement
        self.x += self.dx*tick
        self.y += self.dy*tick

        #looparound
        if(self.x > 800):
            self.x -=832
        if(self.y > 600):
            self.y -=632
        if(self.x < -32):
            self.x +=832
        if(self.y < -32):
            self.y +=632
        
        #updating bounds
        self.bounds = (self.x,self.y,32,32)
        
        

#initialising
bullets = []
tonks = {}

tk = tonk(20,20,createcol(0),'Vany')
tk2 = tonk(800-20-32,600-20-32,createcol(180),'Vany2')
tonks['Vany'] = tk
tonks['Vany2'] = tk2


klok = pygame.time.Clock()
FPS = 60

play = True
while play:
    ms = klok.tick(FPS)
    tick = ms/20.0
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            play = False 
        if event.type == pygame.KEYUP:
            k = event.key
            #movement for 1st tank
            if k == pygame.K_RIGHT or k == pygame.K_LEFT:
                tk.dx = 0
            if k == pygame.K_DOWN or k == pygame.K_UP:
                tk.dy = 0
            #movement for 2nd tank
            if k == pygame.K_d or k == pygame.K_a:
                tk2.dx = 0
            if k == pygame.K_s or k == pygame.K_w:
                tk2.dy = 0
        
        if event.type == pygame.KEYDOWN:
            #movement for 1st tank
            if event.key == pygame.K_DOWN:
                tk.dx = 0
                tk.dy = speed
            if event.key == pygame.K_UP:
                tk.dx = 0
                tk.dy = -speed
            if event.key == pygame.K_LEFT:
                tk.dx = -speed
                tk.dy = 0
            if event.key == pygame.K_RIGHT:
                tk.dx = speed
                tk.dy = 0
            if event.key == pygame.K_SPACE:
                tk.shoot()
            #movement for 2st tank
            if event.key == pygame.K_s:
                tk2.dx = 0
                tk2.dy = speed
            if event.key == pygame.K_w:
                tk2.dx = 0
                tk2.dy = -speed
            if event.key == pygame.K_a:
                tk2.dx = -speed
                tk2.dy = 0
            if event.key == pygame.K_d:
                tk2.dx = speed
                tk2.dy = 0
            if event.key == pygame.K_LSHIFT:
                tk2.shoot()

    #applying changes:
    tk.move()
    tk2.move()

    #redraw
    screen.fill((0,0,0))
    
    #draw bullets
    for b in bullets:
        b.move()
        b.draw()

    #draw tanks
    for k in tonks:
        #check bullet collision
        for b in bullets:
            #check if bullet outside the room
            if(b.x > 810 or b.x < -10 or b.y > 610 or b.y < 0):
                bullets.remove(b)
            elif(intersect(b.bounds,tonks[k].bounds)):
                tonks[k].health -= 1
                bullets.remove(b)
        tonks[k].draw()

    pygame.display.flip()