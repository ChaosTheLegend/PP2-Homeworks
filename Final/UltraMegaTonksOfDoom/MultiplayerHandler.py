import NetworkHandler as net
import ClassHandler as ch
import GraphicsHelper as gh
import ResourceLoader as rs
import AIhandler as AIH
import json
import pygame
import threading
import random

SplashFont = pygame.font.Font('freesansbold.ttf', 50)
ScoreFont = pygame.font.Font('freesansbold.ttf', 34)
DescFont = pygame.font.Font('freesansbold.ttf', 44)
shotsnd = rs.LoadSound('Shot.ogg')

directions = {'UP':0,'RIGHT':1,'DOWN':2,'LEFT':3}
token = ''
tonkid = ''
screen = ''
color = gh.createcol(0)
AI = False
AIs = {'GladOS':(200,200),'Tomas the dank engine':(500,100),'Копатыч':(10000,1),'Tonkinator':(240,140),'Bender':(300,140)}
tonks = {}
bullets = []
scores = {}
rt = 0
cansend = True
gamestate = 0 #0- loading 1 - game in progress 2 - game lost 3 - game won 4 - kicked
play = False
AIcon = ''
AIname = ''
romid = 1
loadstatus = 'Establishing Connection'
loadstage = 0

def Restart():
    global tonks
    global bullets
    global scores
    global rt
    global gamestate
    global loadstatus
    global loadstage

    loadstage = 0
    net.StopAll()
    tonks = {}
    bullets = []
    scores = {}
    rt = 0
    loadstatus = 'Establishing Connection'
    
    threading._start_new_thread(LoadNetwork,())
    gamestate = 0
        

def Stop():
    global play
    net.StopAll()
    play = False

def ChangeDir(direction):
    global cansend
    cansend = False
    mes = json.dumps({"token":token,"direction":direction})
    net.Post('tank.request.turn', mes)
    cansend = True

def Shoot():
    global cansend
    cansend = False
    mes = json.dumps({"token":token})
    if net.Post('tank.request.fire', mes):
        tonks[tonkid].shoottm = 999
    cansend = True


def UnpackEvent(body):
    global rt
    global tonks
    global bullets
    global gamestate
    global AI

    event = json.loads(body)
    gf = event['gameField']
    hits = event['hits']
    wins = event['winners']
    lose = event['losers']
    kicked = event['kicked']
    
    if gamestate != 1:
        return

    if 'remainingTime' in event:
        rt = event['remainingTime']
    
    tks = gf['tanks']
    bls = gf['bullets']

    for k in kicked:
        tonks.pop(k['tankId'])
        if(k['tankId'] == tonkid):
            gamestate = 4
        else:
            scores.pop(k['tankId'])
        
    for l in lose:
        tonks.pop(l['tankId'])
        if(l['tankId'] == tonkid):
            gamestate = 2
        else:
            scores.pop(l['tankId'])
        

    for w in wins:

        if(w['tankId'] == tonkid):
            gamestate = 3
        else:
            scores.pop(w['tankId'])
            
    for tk in tks:
        if not tk['id'] in tonks:
            if tk['id'] == tonkid:
                temptonk = ch.tonk(tk['x']-32,tk['y']-32,color,'You',tk['score'])
            else:
                temptonk = ch.tonk(tk['x']-32,tk['y']-32,gh.createcol(random.randrange(0,360)),tk['id'],tk['score'])
            temptonk.dir = directions[tk['direction']]
            temptonk.health = tk['health']
            tonks[tk['id']] = temptonk
        else:
            tonks[tk['id']].x = tk['x']-32
            tonks[tk['id']].y = tk['y']-32
            tonks[tk['id']].dir = directions[tk['direction']]
            tonks[tk['id']].health = tk['health']
            scores[tk['id']] = tk['score']
        if(AI):
            tonks[tk['id']].tonks = tonks

    lastbulls = len(bullets)
    bullets = []
    for bl in bls:
        tempbul = ch.mpbullet(bl['x']-32,bl['y']-32,bl['width'],bl['height'],directions[bl['direction']],bl['owner'])
        if(bl['owner'] == tonkid):
            tempbul.col = (255,255,0)
        bullets.append(tempbul)
        if(AI):
            tonks[tk['id']].bullets = bullets
    pass
    if(len(bullets) > lastbulls):
        shotsnd.play()

UpdateClock = pygame.time.Clock()

FPS = 60
lastkey = 100  #dont change this please for god's sake!
checkdelay = 100
def DrawScreen():
    global lastkey
    global checkdelay
    global loadstage

    while play:
        ms = UpdateClock.tick(FPS)
        tick = ms/1000
        lastkey -= ms
        checkdelay -= ms
        events = pygame.event.get()
        if(not AI and gamestate == 1):
            for event in events:  
                if event.type == pygame.QUIT: 
                    net.StopAll()
                    exit()
                if lastkey <= 0:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            lastkey = 100
                            if cansend:
                                threading._start_new_thread(ChangeDir, tuple(['DOWN']))

                        elif event.key == pygame.K_UP:
                            lastkey = 100
                            if cansend:
                                threading._start_new_thread(ChangeDir, tuple(['UP']))

                        elif event.key == pygame.K_LEFT:
                            lastkey = 100
                            if cansend:
                                threading._start_new_thread(ChangeDir, tuple(['LEFT']))
                        
                        elif event.key == pygame.K_RIGHT:
                            lastkey = 100
                            if cansend:
                                threading._start_new_thread(ChangeDir, tuple(['RIGHT']))
                    
                        elif event.key == pygame.K_SPACE:
                            lastkey = 100
                            if cansend and tonks[tonkid].shoottm <= 0:
                                threading._start_new_thread(Shoot, ())
            
        screen.fill((0,0,0))
        if(gamestate == 1):
            gh.DrawText(str(rt),SplashFont,(255,255,255),(400,40),screen)
            for bl in bullets:
                bl.move(tick)    
                bl.draw(screen)
            if(AI):
                try:
                    tonks[tonkid].tonks = tonks
                    tonks[tonkid].bullets = bullets
                except:
                    pass

            try:
                for tk in tonks:
                    tonks[tk].dirmove(tick)
                    tonks[tk].draw(screen)
                    tonks[tk].update(ms/40)
            except:
                pass

            pygame.draw.rect(screen, (140,140,140), (800-32,0,200+32,800-32))
            gh.DrawText('Liderboard:',ScoreFont,(255,255,255),(900-16,40),screen)
            i=0
            scorelist = []
            for s in scores:
                scorelist.append((s,scores[s]))
            scorelist.sort(key=lambda tup: tup[1],reverse=True)
            for s in scorelist:
                if s[0] == tonkid:
                    txt = 'You:'+str(s[1])
                else:
                    txt = s[0]+':'+str(s[1])
                
                tx = ScoreFont.render(txt, True, tonks[s[0]].col)
                txRect = tx.get_rect() 
                txRect.x = 1014-16-200
                txRect.y = 64+40*i
                screen.blit(tx, txRect)

                #gh.DrawText(txt,ScoreFont,tonks[s[0]].col,(1100-16,80+40*i),screen)
                gh.DrawHealthbar(980-200,65+40*i,14,28,tonks[s[0]].health,3,3,False,screen)
                i+=1

            if(AI and cansend):
                act = tonks[tonkid].getAction()
                if(act == 'TrunRight'):
                    threading._start_new_thread(ChangeDir, tuple(['RIGHT']))
                if(act == 'TrunLeft'):
                    threading._start_new_thread(ChangeDir, tuple(['LEFT']))
                if(act == 'TrunDown'):
                    threading._start_new_thread(ChangeDir, tuple(['DOWN']))
                if(act == 'TrunUp'):
                    threading._start_new_thread(ChangeDir, tuple(['UP']))
                if(act == 'Fire'):
                    threading._start_new_thread(Shoot, ())

        if(gamestate == 2):
            gh.DrawText('Game Over',SplashFont,(255,255,255),(500,200),screen)
            gh.DrawText('Your score:'+str(scores[tonkid]),DescFont,(255,255,255),(500,280),screen)
        if(gamestate == 3):
            gh.DrawText('You Win!',SplashFont,(255,255,255),(500,200),screen)
            gh.DrawText('Your score:'+str(scores[tonkid]),DescFont,(255,255,255),(500,280),screen)
        if(gamestate == 4):
            gh.DrawText('Disconected',SplashFont,(255,255,255),(500,200),screen)
            gh.DrawText('You\'ve been kicked for AFK',DescFont,(255,255,255),(500,280),screen)
        if(gamestate == 5):
            gh.DrawText('Cannot Connect to server',SplashFont,(255,255,255),(500,200),screen)
            gh.DrawText('Maybe something wrong with your internet?',DescFont,(255,255,255),(500,280),screen)
        if(gamestate > 1):
            gh.DrawButton(400,400,200,40,(140,140,140),(200,200,200),ScoreFont,'Restart',(255,255,255),Restart,screen,events)
            gh.DrawButton(380,460,240,40,(140,140,140),(200,200,200),ScoreFont,'Back to menu',(255,255,255),Stop,screen,events)
        if(gamestate == 0):
            gh.DrawText('Connecting to the server',SplashFont,(255,255,0),(500,140),screen)
            gh.DrawText(loadstatus,DescFont,(255,255,255),(500,270),screen)
            gh.DrawHealthbar(100,330,800,40,loadstage,4,0,True,screen,(0,255,0))
            if(checkdelay <= 0):
                threading._start_new_thread(StatusChecker,())
                checkdelay = 100
            #Restart() #Auto-Restart

        

        pygame.display.flip()
    
def StatusChecker():
    global loadstatus
    global loadstage
    loadstatus = net.CheckStatus()
    if(loadstatus == 'Establishing Connection'):
        loadstage = 0
    if(loadstatus == 'Checking server status'):
        loadstage = 1
    if(loadstatus == 'Joining room'):
        loadstage = 2
    if(loadstatus == 'Getting room events'):
        loadstage = 3
    if(loadstatus == 'Connected!'):
        loadstage = 4
        

def LoadNetwork():
    global token
    global tonkid
    global room
    global gamestate
    global color
    
    respond = net.Register(romid,UnpackEvent)
    if(respond == 'Error'):
        gamestate = 5
        return
    token = respond['token']
    tonkid = respond['tonkid']
    room = respond['roomid']
    ChangeDir('UP')
    if(AI):
        tonks[tonkid] = AIH.AItonk(0,0,color,tonkid,0,AIname,AIs[AIname][0],AIs[AIname][1],AIcon)
    
    gamestate = 1
    
    
def Start(col,rmid,ai = False,aicon = None,ainame = ''):
    global tonks
    global bullets
    global scores
    global rt
    global gamestate
    global screen
    global color
    global play
    global AI
    global tonks
    global AIcon
    global AIname
    global romid
    global loadstatus

    loadstatus = 'Establishing Connection'
    color = col
    romid = rmid
    tonks = {}
    bullets = []
    scores = {}
    rt = 0
    threading._start_new_thread(LoadNetwork,())
    gamestate = 0
    play = True
    
    AI = ai
    screen = pygame.display.set_mode((1000,600-32))
    if(ai):
        AIname = ainame
        AIcon = aicon
       
    DrawScreen()
