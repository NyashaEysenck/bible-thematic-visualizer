import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

client = None
db = None

def get_db():
   """
   Initializes and returns the MongoDB database connection.
   """
   global client, db
   if client is None:
       client = MongoClient(MONGO_DB_URI)
       db = client["bible_rag_db"]
   return db

def close_db_connection():
   """
   Closes the MongoDB connection if it's open.
   """
   global client
   if client:
       client.close()
       client = None