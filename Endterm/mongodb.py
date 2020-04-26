import pymongo
import ssl

client = pymongo.MongoClient("mongodb+srv://VanyAdmin:Vanypass@cluster0-mhy2m.mongodb.net/test?retryWrites=true&w=majority")
print(client.list_database_names())
db = client['ExampleBase']
col = db['ExampleCol']
mystd = {'name':'vany','age': '18'}
x = col.insert_one(mystd)
print('inserted')