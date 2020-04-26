import pika
import sys
from threading import Thread
import pygame
import colorsys
import json
import random

players = {}
pygame.init()
screen = pygame.display.set_mode((1200,900))
speed = 5

name = 'Vany'
ip = 'localhost'

localplayer = {}

nickfont = pygame.font.Font('freesansbold.ttf', 14)

class player():
    def __init__(self,x,y,col,nick):
        self.x = x
        self.y = y
        self.col = col
        self.dx = 0
        self.dy = 0
        self.nick = nick

    def implace(self,x,y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.dx*tick
        self.y += self.dy*tick

    def draw(self):
        pygame.draw.circle(screen, self.col, (int(self.x),int(self.y)), 10, 0)
        text = nickfont.render(self.nick, True, (255,255,255))
        textRect = text.get_rect() 
        textRect.center = (int(self.x), int(self.y-22))
        screen.blit(text, textRect)

connection = pika.BlockingConnection(pika.ConnectionParameters(ip))
prodchennel = connection.channel()
        
class Producer(Thread):
        
    def run(self):
        prodchennel.exchange_declare(exchange='logs',exchange_type='fanout')

    def sendmessage(self,message):
        #print(message)
        prodchennel.basic_publish(exchange='logs',routing_key='',body=message)

    def close(self):
        prodchennel.close()


class Consumer(Thread):
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(ip))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='logs',exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='logs', queue=queue_name)
        
        def callback(ch,method,properties,body):
            parsedjs = json.loads(body)
            pl = parsedjs
            for k in pl:
                if(str(k).count(name) == 0):
                    if k in players: 
                        players[k].x = pl[k]['x']
                        players[k].y = pl[k]['y']
                    else:
                        newp = player(pl[k]['x'],pl[k]['y'],createcol(random.randrange(0,360)),k)
                        players[k] = newp
                        print(k+' Joined the game')

        self.channel.basic_consume(queue=queue_name,on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
    
    def close(self):
        self.channel.close()



def createcol(h):
    col = colorsys.hsv_to_rgb(h/360, 1.0, 1.0) 
    return (col[0]*255,col[1]*255,col[2]*255) 

prd = Producer()
prd.start()
con = Consumer()
con.start()

myplayer = player(100,100,createcol(0),name)
players[name] = myplayer

klok = pygame.time.Clock()
FPS = 60
while True:
    ms = klok.tick(FPS)
    tick = ms/20.0
    for event in pygame.event.get(): # this empties the event queue. 
        if event.type == pygame.QUIT: 
            prd.close()
            con.close()
            break
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                myplayer.dy = speed
            if event.key == pygame.K_UP:
                myplayer.dy = -speed
            if event.key == pygame.K_LEFT:
                myplayer.dx = -speed
            if event.key == pygame.K_RIGHT:
                myplayer.dx = speed
        if event.type == pygame.KEYUP:
            k = event.key
            if k == pygame.K_RIGHT or k == pygame.K_LEFT:
                myplayer.dx = 0
            if k == pygame.K_DOWN or k == pygame.K_UP:
                myplayer.dy = 0
            
    myplayer.move()
    players[name] = myplayer
    screen.fill((0,0,0))

    localplayers = list(players.values())

    for p in range(len(localplayers)):
        try:
            localplayers[p].draw()
        except expression as identifier:
            pass
        
    localplayer = {name:{'x':myplayer.x,'y':myplayer.y}}
    pygame.display.flip()
    if(myplayer.dx != 0 or myplayer.dy != 0):
        prd.sendmessage(json.dumps(localplayer))



            