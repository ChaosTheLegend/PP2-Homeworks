import os
import pymongo
import ssl


client = pymongo.MongoClient("mongodb+srv://VanyAdmin:Vanypass@cluster0-mhy2m.mongodb.net/test?retryWrites=true&w=majority")
#print(client.list_database_names())
db = client['TestBase']
table = db['MyDicks']


clear = lambda: os.system('cls')
clear()
print('Welcome to big biba metagame!')
print('Today we will finally find out who has the biggest biba of them all!')
name = str(input('Please Enter your name:'))
clear = lambda: os.system('cls')
clear()
print('Hello '+name+'!')
print('In order to start playing, you first need to mesure your biba!')
lenth = float(input('Please Enter your biba\'s lenth(in centimeters):'))
width = float(input('Please Enter your biba\'s width(in centimeters):'))
hon = str(input('Are you being honest?:')).strip()
while(hon.lower() != 'yes' and hon.lower() != 'no'):
    print('I don\'t understand you, please say yes or no')
    hon = str(input('Are you being honest?:')).strip()

if(hon.lower() == 'no'):
    clear = lambda: os.system('cls')
    clear()
    print('Yòu̵ ͞h̶ave ̢m͟a͝de a ͜very̷ ͟b͠ig m͘i͜sţàk̨e!͟')
    input('...')
    clear = lambda: os.system('cls')
    clear()
    print('W̶e ̕d͜on̡\'t̢ for͡giv͠e such̷ ̡bl̸u̢n̢d̢e̶r̡s!̨')
    input('...')
    clear = lambda: os.system('cls')
    clear()
    print('Y̸ou̷ wil̵l̸ pay ̡f͝or̢ ̀your͡ ̴c͘ŗim͞es̴!')
    input('...')
    clear = lambda: os.system('cls')
    clear()
    print('Y̧O̴U ͠H̵AV̛E̕ ͠LOST̀ ̧Y͟OUR̸ ̧B͡I͜B͟A̡ ͝PRI̧V̛IL͠ÉG͏E͘!!!̀')
    scis = '''
   _       ,/'
  (_).  ,/'
   _  ::
  (_)'  `\.
           `\. '''
    print(scis)
    input()
    raise SystemExit

def truescore(len, wid):
    avrlen = 14    
    avrwid = 3.8
    lendif = 0
    widdif = 0
    truelen = len
    truewid = wid
    if(len > avrlen):
        lendif = len-avrlen
        truelen = avrlen + lendif**0.5
    if(wid > avrwid):
        widdif = wid-avrwid
        truewid = avrwid + widdif**0.7
    score = truelen*((truewid/2)**2)*3.14
    return score

print('Thank you for sharing, now we will do some calculations to determine how big is your biba!')
input('Press Enter to continue')
clear = lambda: os.system('cls')
clear()
score = truescore(lenth,width)
score = round(score,2)
print('Your score is:'+str(score)+' points!')
if(score < 0):
    print('What! Look\'s like you have anti-biba, I only heard about it in legends, go and finish your quest Bibaborn!')
elif(score > 10000):
    print('You have a godlike biba, the one true biba to rule them all!') 
elif(score > 250):
    print('Your biba is humongous, be proud of it!')
elif(score > 200):
    print('Your biba is large, respect that!')
elif(score > 140):
    print('Your biba is average size, It\'s still impressive nevertheless')
elif(score > 90):
    print('Your biba is quite small, don\'t worry, it\'s better than nothing')
elif(score > 20):
    print('Your biba is miniscule, it\'s better to not have a biba than having such as yours')
else:
    print('Why do you even try, at this point, it\'s not even a biba...')

input('Press Enter to continue')
clear = lambda: os.system('cls')
clear()
ans = input('Would you like to compare your biba with others?').strip()
while(ans.lower() != 'yes' and hon.lower() != 'no'):
    print('I don\'t understand you, please say yes or no')
    hon = str(input('Would you like to compare your biba with others?')).strip()
if(ans.lower() == 'no'):
    exit()

print('Connecting to the database...')
hisdick = {'name': name, 'score': score}
table.insert_one(hisdick)
dicks = table.find().sort('score',-1).limit(5)
alldicks = table.find().sort('score',-1)
dicks = list(dicks)
place = 0
alldicks = list(alldicks)
for a in range(len(alldicks)):
    if(alldicks[a]['name'] == hisdick['name'] and alldicks[a]['score'] == hisdick['score']):
        place = a+1
        break

clear = lambda: os.system('cls')
clear()
print('Scoreboard:')
for i in range(len(dicks)):
    print(str(i+1)+': ' +dicks[i]['name']+' '+str(dicks[i]['score']))
print('Your Score:')
print(str(place) +': '+hisdick['name'] + ' ' +str(hisdick['score']))
input('Press Enter to exit')