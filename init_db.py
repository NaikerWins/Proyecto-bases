import os 

from pymongo import MongoClient, ASCENDING 

from dotenv import load_dotenv 

 

load_dotenv() 

 

client = MongoClient(os.getenv('MONGODB_URI')) 

db = client[os.getenv('DB_NAME')] 

 

# Crear colecciones con validacion de esquema 

if 'chunks' not in db.list_collection_names(): 

    db.create_collection('chunks', validator={ 

        '$jsonSchema': { 

            'bsonType': 'object', 

            'required': ['doc_id','chunk_index','estrategia_chunking', 

                         'chunk_texto','embedding','modelo','fecha_ingesta'], 

            'properties': { 

                'estrategia_chunking': { 

                    'bsonType': 'string', 

                    'enum': ['fixed-size','sentence-aware','semantic'] 

                }, 

                'embedding': { 'bsonType': 'array', 

                               'minItems': 384, 'maxItems': 384 } 

            } 

        } 

    }, validationLevel='moderate', validationAction='warn') 

    print('[OK] Coleccion chunks creada con validacion.') 

 

if 'documents' not in db.list_collection_names(): 

    db.create_collection('documents', validator={ 

        '$jsonSchema': { 

            'bsonType': 'object', 

            'required': ['doc_code','title','category','text','date_ingested'] 

        } 

    }, validationLevel='moderate', validationAction='warn') 

    print('[OK] Coleccion documents creada con validacion.') 

 

# Crear indices tradicionales 

db.chunks.create_index([('category', ASCENDING)]) 

db.chunks.create_index([('estrategia_chunking', ASCENDING)]) 

db.chunks.create_index([('doc_id', ASCENDING)]) 

db.chunks.create_index([('fecha_ingesta', ASCENDING), ('language', ASCENDING)]) 

db.documents.create_index([('text', 'text')])  # full-text index 

print('[OK] Indices tradicionales creados.') 

print('[INFO] Crea el indice vectorial manualmente en Atlas Vector Search.') 