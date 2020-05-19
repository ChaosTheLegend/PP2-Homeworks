import pygame
import ClassHandler as ch
import GraphicsHelper as gh
import math
import random
import ResourceLoader as rs

gamestate = 1
buttonfont = pygame.font.Font('freesansbold.ttf', 26)
titlefont = pygame.font.Font('freesansbold.ttf', 40)
p1col = ''
p2col = ''
play = True
tk1 = ''
tk2 = ''
powertimer = 0
powerup = None
bullets = []
blocks = []
lvl = ''
lvlname = ''
repairsound = rs.LoadSound('Repair.ogg')

brickimg = rs.LoadImage('brick.png')
woodimg = rs.LoadImage('wood.png')


def intersect(colbox1,colbox2):
     return(colbox2[0] <= colbox1[0]+colbox1[2] and colbox2[1] <= colbox1[1]+colbox1[3]) and (colbox2[0]+colbox2[2] >= colbox1[0] and colbox2[1]+colbox2[3] >= colbox1[1])

def Menu():
    global play
    play = False

def Restart():
    global gamestate
    global tk1
    global tk2
    global powertimer
    global powerup
    global bullets
    global lvl

    gamestate = 1
    powertimer = random.randrange(5000,10000)
    powerup = None
    bullets = []
    blocks = lvl['map']
    try:
        tk1 = ch.tonk(lvl['players']['1'][0],lvl['players']['1'][1],p1col,'player 1',0)
        tk2 = ch.tonk(lvl['players']['2'][0],lvl['players']['2'][1],p2col,'player 2',0)
    except:
        tk1 = ch.tonk(40,40,p1col,'player 1',0)
        tk2 = ch.tonk(800-40-32,600-32,p2col,'player 2',0)
    

def StartSingleplayer(pcol1,pcol2,level,levelname):
    global gamestate
    global p1col
    global p2col
    global tk1
    global tk2
    global play
    global powertimer
    global powerup
    global bullets
    global blocks
    global lvl
    global lvlname

    gamestate = 1
    play = True

    bullets = []
    lvl = level
    blocks = level['map']
    lvlname = levelname


    p1col = pcol1
    p2col = pcol2
    
    screen = pygame.display.set_mode((800,640))
    try:
        tk1 = ch.tonk(level['players']['1'][0],level['players']['1'][1],pcol1,'player 1',0)
        tk2 = ch.tonk(level['players']['2'][0],level['players']['2'][1],pcol2,'player 2',0)
    except:
        tk1 = ch.tonk(40,40,pcol1,'player 1',0)
        tk2 = ch.tonk(800-40-32,600-32,pcol2,'player 2',0)
            
    powerup = None

    powertimer = random.randrange(5000,10000)

    UpdateClock = pygame.time.Clock()
    FPS = 60

    move1 = True
    move2 = True
    while play:
        ms = UpdateClock.tick()
        tick = ms/20.0
        powertimer -= ms
        move1 = True
        move2 = True
    
        if(powertimer <= 0 and powerup == None):
            collide = True
            while collide:
                if levelname == 'HitlerLand':
                    powerup = ch.powerup(random.randrange(50,750),random.randrange(50,550),3)
                else:
                    #powerup = ch.powerup(random.randrange(50,750),random.randrange(50,550),2)
                    powerup = ch.powerup(random.randrange(50,750),random.randrange(50,550),int(random.randrange(1,3)))
                collide = False
                for bl in blocks:
                    if(intersect(powerup.bounds,bl.bounds)):
                        collide = True
                        break


        events = pygame.event.get()
        for event in events:  
            if event.type == pygame.QUIT: 
                return False
            if event.type == pygame.KEYDOWN:
                #movement for 1st tank
                if event.key == pygame.K_DOWN:
                    tk1.dx = 0
                    tk1.dy = 1
                if event.key == pygame.K_UP:
                    tk1.dx = 0
                    tk1.dy = -1
                if event.key == pygame.K_LEFT:
                    tk1.dx = -1
                    tk1.dy = 0
                if event.key == pygame.K_RIGHT:
                    tk1.dx = 1
                    tk1.dy = 0
                if event.key == pygame.K_SPACE:
                    bl = tk1.shoot()
                    if(bl != None):
                        bullets.append(bl)
                #movement for 2st tank
                if event.key == pygame.K_s:
                    tk2.dx = 0
                    tk2.dy = 1
                if event.key == pygame.K_w:
                    tk2.dx = 0
                    tk2.dy = -1
                if event.key == pygame.K_a:
                    tk2.dx = -1
                    tk2.dy = 0
                if event.key == pygame.K_d:
                    tk2.dx = 1
                    tk2.dy = 0
                if event.key == pygame.K_LSHIFT:
                    bl = tk2.shoot()
                    if(bl != None):
                        bullets.append(bl)
        nextbounds1 = (tk1.x+tk1.dx*2.5,tk1.y+tk1.dy*2.5,32,32)
        nextbounds2 = (tk2.x+tk2.dx*2.5,tk2.y+tk2.dy*2.5,32,32)
        
        

        if(tk1.x > 800):
            tk1.x -=832
        if(tk1.y > 640):
            tk1.y -=632+40
        if(tk1.x < -32):
            tk1.x +=832
        if(tk1.y < -32):
            tk1.y +=632+40
        
        if(tk2.x > 800):
            tk2.x -=832
        if(tk2.y > 640):
            tk2.y -=632+40
        if(tk2.x < -32):
            tk2.x +=832
        if(tk2.y < -32):
            tk2.y +=632+40
        


        screen.fill((0,0,0))
        if(gamestate == 1):
            tk1.update(tick)
            tk2.update(tick)

            for bl in blocks:
                bl.draw(screen)
                if(intersect(nextbounds1,bl.bounds)):
                    move1 = False
                if(intersect(nextbounds2,bl.bounds)):
                    move2 = False
                for b in bullets:
                    if(intersect(b.bounds,bl.bounds)):
                        if(bl.hp != -100):
                            bl.hp -=1
                            if(bl.hp <= 0):
                                blocks.remove(bl)
                        bullets.remove(b)
            
            tk1.draw(screen)
            tk2.draw(screen)
            
            if(powerup != None):
                powerup.draw(screen)
                if(intersect(powerup.bounds,tk1.bounds)):
                    powertimer = random.randrange(5000,10000)
                    if powerup.type == 1:
                        tk1.powertm = 5000
                        tk1.speed *= 2
                    if powerup.type == 2:
                        tk1.health += 1
                        tk1.health = min(3,tk1.health)
                        repairsound.play()
                    if powerup.type == 3:
                        tk1.hitler = True
                        tk1.delay = 0
                        tk1.health = 10
                    powerup = None         
                elif(intersect(powerup.bounds,tk2.bounds)):
                    powertimer = random.randrange(5000,10000)
                    if powerup.type == 1:
                        tk2.powertm = 5000
                        tk2.speed *= 2
                    if powerup.type == 2:
                        tk2.health += 1
                        tk2.health = min(3,tk2.health)
                        repairsound.play()
                    if powerup.type == 3:
                        tk2.hitler = True
                        tk2.delay = 0
                        tk2.health = 10
                        
                    powerup = None
                    
            if(intersect(nextbounds1,tk2.bounds)):
                move1 = False
            if(intersect(nextbounds2,tk1.bounds)):
                move2 = False

            if(move1):
                tk1.move(tick)
            if(move2):
                tk2.move(tick)
            
            for b in bullets:
                b.move(tick)
                if(b.x > 810 or b.x < -10 or b.y > 650 or b.y < 0):
                    bullets.remove(b)
                elif(intersect(b.bounds,tk1.bounds)):
                    if(b.owner != tk1.nick):
                        tk1.health -= 1
                        bullets.remove(b)
                elif(intersect(b.bounds,tk2.bounds)):
                    if(b.owner != tk2.nick):
                        tk2.health -= 1
                        bullets.remove(b)
                
                b.draw(screen)
            if(tk1.health == 0 or tk2.health == 0):
                tk1.shoottm = 1000
                tk2.shoottm = 1000
                gamestate = 0
        if gamestate == 0:
            winp = '... What, This text should not appear'
            if(tk2.health == 0):
                winp = '1'
            if(tk1.health == 0):
                winp = '2'
                
            gh.DrawText('Player'+winp+' Wins!',titlefont,(255,255,255),(400,100),screen)
            gh.DrawButton(300,240,200,40,(100,100,100),(180,180,180),buttonfont,'Restart',(255,255,255),Restart,screen,events)
            gh.DrawButton(300,300,200,40,(100,100,100),(180,180,180),buttonfont,'Back to menu',(255,255,255),Menu,screen,events)

        pygame.display.flip()
    return True   