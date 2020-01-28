import os.path
from pathlib import Path

globhit = False
exit = "exit"
def default(path):
    newpath = ''
    if os.path.isfile(path):
        newpath = fileper(path)
    else:
        newpath = diroper(path)
    return newpath

def getdirnum(path):
    files = os.listdir(path)
    num = 0
    for fl in files:
        flpath = os.path.join(path,fl)
        if(os.path.isdir(flpath)):
            num+=1
    print("There are currently",num,"folders in this directory")
    return path

def getfilenum(path):
    files = os.listdir(path)
    num = 0
    for fl in files:
        flpath = os.path.join(path,fl)
        if(os.path.isfile(flpath)):
            num+=1
    print("There are currently",num,"files in this directory")
    return path

def init():
    clear = lambda: os.system('cls')
    clear()
    if(globhit):
        print('--卐卐--Welcome to Hitlerland!--卐卐--')
    else:
        print('-------Welcome to Ivans file manager!-------')
        
def refresh(path):
    print("press enter to continue")
    input()
    clear = lambda: os.system('cls')
    clear()
    if(globhit):
        print('--卐卐--卐卐--卐卐--卐卐--卐卐--卐卐--卐卐--')
    else:
        print("------------------------------------")

def rename(path):
    file = os.path.basename(path)
    print("Old name:" + file)
    name = input("Enter new filename:")
    ps = Path(path)
    parent = ps.parent
    newps = os.path.join(parent,name)
    os.rename(path,newps)
    return newps

def showdir(path):
    print("-----------------------------")
    ls = os.listdir(path)
    print("Directory",path,"Contains:")
    for fl in ls:
        print(fl)
    return path

def createfile(path):
    print("-----------------------------")
    print("Current Directory:", path)
    name = input("Enter new file name:")
    newps = os.path.join(path,name)
    f = open(newps, 'w+')
    f.close()
    return newps

def createfolder(path):
    print("Current Directory:", path)
    name = input("Enter new folder name:")
    newps = os.path.join(path,name)
    os.mkdir(newps)
    return newps

def printhit():
    clear = lambda: os.system('cls')
    clear()
    hitler = """    ░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░▓▓▀▀██████▓▄▒▒░░░░░░░░░
    ░░░▀░░░░░░▀▀▀████▄▒░░░░░░░░
    ░░▌░░░░░░░░░░░▀███▓▒░░░░░░░
    ░▌░░░░░▄▄▄░░░░░░▐█▓▒░░░░░░░
    ░▄▓▀█▌░▀██▀▒▄░░░▐▓▓▓▒░░░░░░
    ░█▌░░░░░▀▒░░░▀░░░▐▓▒▒░░░░░░
    ░▌▀▒▄▄░░░░░░░░░░░░░▄▒░░░░░░
    ░▒▄█████▌▒▒█░█▀▀░░░▒▌▒░░░░░
    ░░▓█████▄▒░▀▀█▀█░░░▐░░░░░░░
    ░░▒▀▓▒▒▒░░░▀▀▀░▀▒▒░▒▒▒▄░░░░
    ░░▓▒▒▒░░░░░░▒▒▒▒▒░▓░░░░░░░░
    ░░████▄▄▄▄▓▓▓▒▒░░▐░░░░░░░░░
    ░░░▀██████▓▒▒▒▒▒░▐░░░░░░░░░"""
    print(hitler)
    return 'hitler'
    

def diroper(path):
    print("Current path:", path)
    print("Choose an operation:")
    driveless = ''
    driveless = os.path.splitdrive(path)
    if(driveless[1] != ''):
        ops = {1: 'rename directory', 2: 'get number of files', 3: 'get number of directories', 4: 'show directory contance', 5: 'create file', 6: 'create directory', 7: exit
        }
    else:
        ops = {1: 'get number of files', 2: 'get number of directories', 3: 'show directory contance', 4: 'create file', 5: 'create directory', 6: exit}

    for k in ops:
        st = ''+str(k)+'-'+ops[k]
        print(st)
    i = getoperation()
    newpath = ""
    
    if(i == 'hitler'):
            return printhit()
    else:
        i = int(i)
    
    if(driveless[1] == ''):
        i+=1

    if(i == 1):
        newpath = rename(path)
    elif(i == 2):
        newpath = getfilenum(path)
    elif(i == 3):
        newpath = getdirnum(path)
    elif(i == 4):
        newpath = showdir(path)
    elif(i == 5):
        newpath = createfile(path)
    elif(i == 6):
        newpath = createfolder(path)
    elif(i == 7):
        newpath = 'kill'
    return newpath


def delete(path):
    ps = Path(path)
    parentdir = ps.parent
    os.remove(ps)
    print("File was succesfully deleted")
    return parentdir

def getparent(path):
    ps = Path(path)
    par = ps.parent
    return par

def addfile(path):
    print("------------------------------------")
    toadd = input('Enter what to add to file:')
    file = open(path,'a')
    file.write(toadd)
    file.close()
    return path

def rewritefile(path):
    print("------------------------------------")
    toadd = input('Enter what to add to file:')
    file = open(path,'w')
    file.write(toadd)
    file.close()
    return path

def readfile(path):
    print("------------------------------------")
    file = open(path)
    inside = file.read()
    print(inside)
    return path

def fileper(path):
    print("Current path:", path)
    print("Choose an operation:")
    ops = {1: 'delete file', 2: 'rename file', 3: 'add to file', 4: 'rewrite the file', 5: 'read file', 6: 'get parent directory', 7: exit}
    newpath = ""
    for k in ops:
        st = ''+str(k)+'-'+ops[k]
        print(st)
    i = getoperation()
    if(i == 'hitler'):
        return printhit() 
    else:
        i = int(i)
    
    if(i == 1):
        newpath = delete(path)
    elif(i == 2):
        newpath = rename(path)
    elif(i == 3):
        newpath = addfile(path)
    elif(i == 4):
        newpath = rewritefile(path)
    elif(i == 5):
        newpath = readfile(path)
    elif(i == 6):
        newpath = getparent(path)
    elif(i == 7):
        newpath = 'kill'
    
    return newpath


def getoperation():
    res = input()
    return res

init()
path = "C:"
while (True):
    path = default(path)
    
    if(path == 'kill'):
        clear = lambda: os.system('cls')
        clear()
        break

    if(path == 'hitler'):
        globhit = not globhit
        path = "C:"
        if(globhit):
            exit = 'ausfahrt!'
        else:
            exit = 'exit'
        refresh(path)
        clear = lambda: os.system('cls')
        clear()
        init()
    else:
        refresh(path)