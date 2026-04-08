from pymongo import MongoClient 

import os 

from dotenv import load_dotenv 

 

load_dotenv() 

client = MongoClient(os.getenv('MONGODB_URI')) 

 

# Ping al servidor 

client.admin.command('ping') 

print('[OK] Conexion exitosa a MongoDB Atlas.') 

 

db = client[os.getenv('DB_NAME')] 

print('Base de datos:', db.name) 

print('Colecciones:', db.list_collection_names()) 

print('Indices en chunks:', list(db.chunks.index_information().keys())) 