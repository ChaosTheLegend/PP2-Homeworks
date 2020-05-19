import pika
import sys
import json
import pygame
import uuid
from threading import Thread

ip = '34.254.177.17'
tonkid = ''
roomid = ''
token = ''
serverstatus = 'Undefined'

eventcon = ''
RPC = ''
onEvent = ''
econect = ''
echannel = ''

class RpcClient():

    def __init__(self):
        global channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip,port='5672',virtual_host='dar-tanks',credentials=pika.PlainCredentials(username='dar-tanks',password='5orPLExUYnyVYZg48caMpX')))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True,auto_delete=True)
        self.callback_queue = result.method.queue
        self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=False)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = [props,body]

    def call(self, key, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

       
class EventConsumer(Thread):
    def run(self):
        global onEvent
        global echannel

        result = echannel.queue_declare(queue='', exclusive=True, auto_delete=True)
        queue = result.method.queue
        echannel.queue_bind(exchange='X:routing.topic', queue=queue, routing_key='event.state.'+roomid)
        def callback(ch,method,properties,body):
            onEvent(body)
        echannel.basic_consume(queue=queue,on_message_callback=callback, auto_ack=True)
        echannel.start_consuming()
    
    def stop(self):
        echannel.stop_consuming()
    

def UnpackRespond(respond):
    global serverstatus
    global token
    global tonkid
    global roomid
    message = respond[1]
    properties = respond[0]


    msg = json.loads(message)
    if(properties.type == 'error'):
        print('Server responded with an error!')
        print('Error: '+msg['message'])
        return False
    elif(properties.type == 'response'):
        if('roomId' in msg):
            roomid = msg['roomId']
            token = msg['token']
            tonkid = msg['tankId']
            return True
        elif(msg['status'] == 200):
            return True
        
        
    return False

def Post(key,message):
    global RPC
    return UnpackRespond(RPC.call(key,message))


def StopAll():
    eventcon.stop()

def CheckStatus():
    output = 'Establishing Connection'
    if(RPC != ''):
        output = 'Checking server status'
    if(serverstatus != 'Undefined'):
        output = 'Joining room'
    if(token != ''):
        output = 'Getting room events'
    if(eventcon != ''):
        output = 'Connected!'
    return output

def Register(rmid,event):
    global rescon
    global eventcon
    global prd
    global onEvent
    global RPC
    global econect
    global echannel
    global token
    RPC = ''
    serverstatus = 'Undefined'
    token = ''
    eventcon = ''
    
    econect= pika.BlockingConnection(pika.ConnectionParameters(host=ip,port='5672',virtual_host='dar-tanks',credentials=pika.PlainCredentials(username='dar-tanks',password='5orPLExUYnyVYZg48caMpX')))
    echannel = econect.channel()
    print('Initialising')
    print('Establishing RPC client')
    RPC = RpcClient()
    print('client established!')
    print('Checking server status')
    if not UnpackRespond(RPC.call('tank.request.healthcheck','')):
        return 'error'
    print('Server is up!')
    serverstatus = 'OK'

    i = rmid
    print('Joining: '+'room-'+str(i))
    mes = json.dumps({"roomId":'room-'+str(i)})

    res = UnpackRespond(RPC.call('tank.request.register',mes))
    while res == False:
        i+=1
        if(i == 31):
            print('All servers are full!')
            return
        mes = json.dumps({"roomId":'room-'+str(i)})
        res =  UnpackRespond(RPC.call('tank.request.register',mes))
        
   
   
    print('Joined '+roomid+' as '+tonkid+' with token '+token)
    
    print('Establishing event consumer')
    onEvent = event
    eventcon = EventConsumer()
    eventcon.start()
    print('Event consumer established')
    print('Network has been established!')
    
    return({'token':token,'tonkid':tonkid,'roomid':roomid})

