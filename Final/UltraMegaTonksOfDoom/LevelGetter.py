import pymongo
import sys
import os
import ResourceLoader
import ClassHandler as ch

#getting maps from DB
brickimg = ResourceLoader.LoadImage('brick.png')
woodimg = ResourceLoader.LoadImage('wood.png')

collection = ''


deflevel = []
for row in range(20):
    deflevel.append([])
    for column in range(25):
        deflevel[row].append(".")

def preInit():
    global collection

    client = pymongo.MongoClient("mongodb+srv://Player:guest@cluster0-mhy2m.mongodb.net/test?retryWrites=true&w=majority")
    db = client['TonksDB']
    collection = db['Levels']


def GetLevelNames():
    request = collection.find({},{'_id':0,'name':1})
    output = []
    for x in request:
        output.append(x['name'])
    return output    

def GetAllLevels():
    request = collection.find({},{'_id':0,'name':1,'level':1})
    return request    

    

def GetLevel(name):
    request = collection.find_one({'name':name})
    if(request == None):
        output = deflevel
        print('Level Not Found')    
    else:
        output = request['level']
    return output

def scanmap(level):
    x = 0
    y = 0
    blocks = []
    playerpos = {}
    for row in level:
        for line in row:
            if(line == '#'):
                bl = ch.block(x,y,brickimg,-100)
                blocks.append(bl)
            if(line == '@'):
                bl = ch.block(x,y,woodimg,1)
                blocks.append(bl)
            for i in range(1,5):
                if(line == str(i)):
                    playerpos[str(i)] = (x,y)
            x += 32
        x = 0
        y+= 32
    return {'map':blocks,'players':playerpos}
