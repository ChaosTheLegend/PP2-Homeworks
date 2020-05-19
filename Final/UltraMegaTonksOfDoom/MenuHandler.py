import pygame
import GraphicsHelper as gh
import ResourceLoader as rs
import SinglePlayerHandler as sp
import MultiplayerHandler as mp
import LevelGetter as lvl
import random
import threading
import os

pygame.init()

UpdateClock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600))

titlefont = pygame.font.Font('freesansbold.ttf', 40)
namefont = pygame.font.Font('freesansbold.ttf', 30)
buttonfont = pygame.font.Font('freesansbold.ttf', 26)
levelfont = pygame.font.Font('freesansbold.ttf', 18)
selectedRoom = 1

tonkimg = rs.LoadImage('tonk.png')
bots = []
levels = []
botnames = {'Tonkinator':['hasta la vista, baby'],'Bender':['I\'m gonna make my own tanks,','with blackjack and hookers'],'Tomas the dank engine':['Tomas has seen enough'],'Копатыч':['Укуси меня пчела'],'GladOS':['Killing you and giving you advice','aren\'t mutually exclusive']}
for i in range(5):
    bots.append(rs.LoadImage('bots/bot'+str(i+1)+'.png'))
    
p1col = gh.createcol(0)
p2col = gh.createcol(180)
selectedAI = -1

menuOpen = True
menu = 'Default'
playercols = {'1':(255,0,0),'2':(0,0,255),'3':(0,255,0),'4':(255,255,0)}
def LoadDB():
    global menu
    try:
        lvl.preInit()
    except:
        print('Can\'t connet to database')
        menu = 'Failed'
        return
    lvls = lvl.GetAllLevels()
    for lv in lvls:
        scan = lvl.scanmap(lv['level'])
        blocks = scan['map']
        pos = scan['players']
        lvlpic = pygame.Surface((800,640))
        for bl in blocks:
            lvlpic.blit(bl.sprite,(bl.bounds[0],bl.bounds[1])) 
        for pl in pos:
            pygame.draw.rect(lvlpic,playercols[pl],(pos[pl][0],pos[pl][1],32,32))
            lvlpic.blit(tonkimg,(pos[pl][0],pos[pl][1]))
        
        lvlpic = pygame.transform.scale(lvlpic,(200, 160))
        levels.append({'name':lv['name'],'pic':lvlpic})

#LoadDB()

def Single():
    global menu
    global DBstate
    menu = 'Single'
    
threading._start_new_thread(LoadDB,())
        
def Multi():
    global menu
    menu = 'Multi'

def EnterSingle():
    global menuOpen
    menuOpen = sp.StartSingleplayer(p1col,p2col,lvl.scanmap(lvl.GetLevel(levels[len(levels)-1]['name'])),levels[len(levels)-1]['name'])
    if(menuOpen == True):
        screen = pygame.display.set_mode((600,600))

def EnterMulti():
    mp.Start(p1col,selectedRoom)
    screen = pygame.display.set_mode((600,600))

def SpamAi():
    for i in range(2):
        botid = random.randrange(0,5)
        
        
        #screen = pygame.display.set_mode((600,600))

def AI():
    global menu
    menu = 'AI'

def EnterAI():
    mp.Start((100,100,100),selectedRoom,True,bots[selectedAI],list(botnames.keys())[selectedAI])
    screen = pygame.display.set_mode((600,600))

def Main():
    global menu
    menu = 'Default'

h = 0

def flipforvard():
    global levels
    numb = len(levels)-1
    placeholder = levels[numb]
    levels.pop(numb)
    levels.insert(0,placeholder)    


def flipback():
    global levels
    placeholder = levels[0]
    levels.pop(0)
    levels.append(placeholder)    
    
def fliprandom():
    for i in range(random.randrange(1,len(levels)-1)):
        flipforvard()

def test():
    pass

def roomIncr():
    global selectedRoom
    selectedRoom+=1
    if selectedRoom == 31:
        selectedRoom -= 30

def roomDecr():
    global selectedRoom
    selectedRoom-=1
    if selectedRoom == 0:
        selectedRoom +=30

def roomIncr2():
    global selectedRoom
    selectedRoom+=5
    if selectedRoom >= 31:
        selectedRoom -=30
    
def roomDecr2():
    global selectedRoom
    selectedRoom-=5
    if selectedRoom <= 0:
        selectedRoom +=30

while menuOpen:
    ms = UpdateClock.tick(60)
    h+=ms//10
    h%=360
    events = pygame.event.get()
    for event in events:  
        if event.type == pygame.QUIT: 
            exit() 

    screen.fill((0,0,0)) 
    Splash = ''
    Splashcol = ''
    if(menu == 'Failed'):
        Splash = 'No Internet!'
        Splashcol = (255,0,0)
        gh.DrawText('Sorry, but this game requres',buttonfont,(255,255,255),(300,120),screen)
        gh.DrawText('internet connection to play.',buttonfont,(255,255,255),(300,150),screen)
        gh.DrawText('Please check your connection',buttonfont,(255,255,255),(300,180),screen)
        gh.DrawText('and restart the game.',buttonfont,(255,255,255),(300,210),screen)
        gh.DrawText('If this problem continues, please',buttonfont,(255,255,255),(300,240),screen)
        gh.DrawText('contact Ivan for technical support',buttonfont,(255,255,255),(300,270),screen)
        
        gh.DrawButton(200,540,200,40,(100,100,100),(255,0,0),buttonfont,'Exit',(255,255,255),exit,screen,events)
        
    if(menu == 'Default'):
        Splash = 'Welcome to Ultra Tonks!'
        Splashcol = gh.createcol(h)
        gh.DrawButton(200,160,200,40,(100,100,100),(180,180,180),buttonfont,'Singleplayer',(255,255,255),Single,screen,events)
        gh.DrawButton(200,220,200,40,(100,100,100),(180,180,180),buttonfont,'Multiplayer',(255,255,255),Multi,screen,events)
        gh.DrawButton(200,280,200,40,(100,100,100),(180,180,180),buttonfont,'AI mode',gh.createcol(h),AI,screen,events)
        #gh.DrawButton(200,400,200,40,(100,100,100),(255,0,0),buttonfont,'Spam AI',(255,0,0),SpamAi,screen,events)
        gh.DrawButton(200,340,200,40,(100,100,100),(255,0,0),buttonfont,'Exit',(255,255,255),exit,screen,events)
        
    #Singleplayer
    if(menu == 'Single'):
        Splash = 'Singleplayer:'
        Splashcol = (255,255,255)
        gh.DrawButton(170,530,260,40,(100,100,100),(180,180,180),buttonfont,'Back to Main Menu',(255,255,255),Main,screen,events)
        #Colors:
        gh.DrawText('Select Colors:',buttonfont,(255,255,255),(140,100),screen)
        gh.DrawText('Player 1:',buttonfont,(255,255,255),(140,140),screen)
        gh.DrawText('Player 2:',buttonfont,(255,255,255),(140,280),screen)

        for i in range(120):
            pygame.draw.rect(screen, gh.createcol(i*3), (20+i*2,170,2,30))
            pygame.draw.rect(screen, gh.createcol(i*3), (20+i*2,310,2,30))

        mspos = pygame.mouse.get_pos() 
        if(20 <= mspos[0] <= 20+240 and 170 <= mspos[1] <= 170+30):
            if(pygame.mouse.get_pressed()[0] == 1):
                p1col = gh.createcol(((mspos[0]-20)/240)*360) 

        if(20 <= mspos[0] <= 20+240 and 300 <= mspos[1] <= 300+30):
            if(pygame.mouse.get_pressed()[0] == 1):
                p2col = gh.createcol(((mspos[0]-20)/240)*360) 

        pygame.draw.rect(screen, p1col, (120,220,32,32))
        pygame.draw.rect(screen, p2col, (120,360,32,32))
        screen.blit(tonkimg, (120,220))
        screen.blit(tonkimg, (120,360))
        #Map
        gh.DrawText('Select Map:',buttonfont,(255,255,255),(450,100),screen)
        
        if(len(levels) == 0):
            gh.DrawText('Loading'+'.'*((h//30)%4),buttonfont,(255,255,0),(450,240),screen)
        else:
            gh.DrawButton(515,365,70,30,(100,100,100),(180,180,180),buttonfont,'next',(255,255,255),flipforvard,screen,events)
            gh.DrawButton(315,365,70,30,(100,100,100),(180,180,180),buttonfont,'prev',(255,255,255),flipback,screen,events)
            gh.DrawButton(390,365,120,30,(100,100,100),(180,180,180),buttonfont,'random',(255,255,255),fliprandom,screen,events)
            
            gh.DrawButton(200,440,200,40,(100,100,100),(180,180,180),buttonfont,'Play',(255,255,255),EnterSingle,screen,events)

        offset = 0
        for lv in levels:
            offset+=30/(len(levels)+1)
            screen.blit(lv['pic'],(340+int(offset),170+int(offset)))
            pygame.draw.rect(screen, (120,120,120), (340+int(offset),170+int(offset),200,160),1)
            gh.DrawText(lv['name'],levelfont,(255,255,255),(440+int(offset),310+int(offset)),screen)
            
        
        
    #Multiplayer  
    if(menu == 'Multi'):
        Splash = 'Multiplayer:'
        Splashcol = (255,255,255)
        gh.DrawButton(170,530,260,40,(100,100,100),(180,180,180),buttonfont,'Back to Main Menu',(255,255,255),Main,screen,events)
        gh.DrawButton(200,370,200,40,(100,100,100),(180,180,180),buttonfont,'Play',(255,255,255),EnterMulti,screen,events)
        
        gh.DrawText('Select Color:',titlefont,(255,255,255),(300,120),screen)
        for i in range(280):
            pygame.draw.rect(screen, gh.createcol(i*(360/280)), (20+i*2,170,2,30))
        
        mspos = pygame.mouse.get_pos() 
        
        if(20 <= mspos[0] <= 20+560 and 170 <= mspos[1] <= 170+30):
            if(pygame.mouse.get_pressed()[0] == 1):
                p1col = gh.createcol(((mspos[0]-20)/560)*360) 

        gh.DrawText('Selected room:',buttonfont,(255,255,255),(300,290),screen)
        pygame.draw.rect(screen, (150,150,150), (300-25,315,50,40), 2)
        gh.DrawText(str(selectedRoom),buttonfont,(255,255,255),(300,335),screen)
        gh.DrawButton(331,315,30,40,(100,100,100),(180,180,180),buttonfont,'>',(255,255,255),roomIncr,screen,events)
        gh.DrawButton(240,315,30,40,(100,100,100),(180,180,180),buttonfont,'<',(255,255,255),roomDecr,screen,events)
        gh.DrawButton(365,315,36,40,(100,100,100),(180,180,180),buttonfont,'>>',(255,255,255),roomIncr2,screen,events)
        gh.DrawButton(200,315,36,40,(100,100,100),(180,180,180),buttonfont,'<<',(255,255,255),roomDecr2,screen,events)

        pygame.draw.rect(screen, p1col, (300-16,230,32,32))
        screen.blit(tonkimg, (300-16,230))
    
    #AI
    if(menu == 'AI'):
        Splash = 'AI Multiplayer:'
        Splashcol = gh.createcol(h)
        mspos = pygame.mouse.get_pos() 
        gh.DrawText('Choose your fighter:',titlefont,(255,255,255),(300,100),screen)
        gh.DrawButton(170,530,260,40,(100,100,100),(180,180,180),buttonfont,'Back to Main Menu',(255,255,255),Main,screen,events)
        i = 0
        selecting = False
        for b in bots:
            b.set_colorkey((2,2,2))
            pygame.draw.rect(screen, (150,150,150), (96+92*i,156,40,40))
            if(96+92*i <= mspos[0] <= 96+92*i+40 and 156 <= mspos[1] <= 196):
                selecting = True
                pygame.draw.rect(screen, (200,200,200), (96+92*i,156,40,40),2)
                gh.DrawText(list(botnames.keys())[i],namefont,(235,235,0),(300,240),screen)
                bottexts = list(botnames.values())
                k = 0
                for l in bottexts[i]:
                    gh.DrawText(l,buttonfont,(255,255,255),(300,280+32*k),screen)
                    k+=1
                if(pygame.mouse.get_pressed()[0] == 1):
                    selectedAI = i
            screen.blit(b,(100+92*i,160))
            i+=1

        if(selectedAI != -1 and not selecting):
            pygame.draw.rect(screen, (235,235,0), (96+92*selectedAI,156,40,40),2)
            gh.DrawText(list(botnames.keys())[selectedAI],namefont,(235,235,0),(300,240),screen)
            bottexts = list(botnames.values())
            k = 0
            for l in bottexts[selectedAI]:
                gh.DrawText(l,buttonfont,(255,255,255),(300,280+32*k),screen)
                k+=1
        
        gh.DrawText('Selected room:',buttonfont,(255,255,255),(300,370),screen)
        pygame.draw.rect(screen, (150,150,150), (300-25,395,50,40), 2)
        gh.DrawText(str(selectedRoom),buttonfont,(255,255,255),(300,415),screen)
        gh.DrawButton(331,395,30,40,(100,100,100),(180,180,180),buttonfont,'>',(255,255,255),roomIncr,screen,events)
        gh.DrawButton(240,395,30,40,(100,100,100),(180,180,180),buttonfont,'<',(255,255,255),roomDecr,screen,events)
        gh.DrawButton(365,395,36,40,(100,100,100),(180,180,180),buttonfont,'>>',(255,255,255),roomIncr2,screen,events)
        gh.DrawButton(200,395,36,40,(100,100,100),(180,180,180),buttonfont,'<<',(255,255,255),roomDecr2,screen,events)

        if(selectedAI == -1 ):
            gh.DrawButton(200,450,200,40,(60,60,60),(100,100,100),buttonfont,'Play',(140,140,140),test,screen,events)
        else:
            gh.DrawButton(200,450,200,40,(100,100,100),(140,140,140),buttonfont,'Play',(255,255,255),EnterAI,screen,events)

        

    gh.DrawText(Splash,titlefont,Splashcol,(300,40),screen)
        
    pygame.display.flip()
