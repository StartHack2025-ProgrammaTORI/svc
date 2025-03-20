from pymongo import MongoClient
import os

DATABASE_URL = os.getenv("DATABASE_URL")
mongo_client = MongoClient(DATABASE_URL)
db = mongo_client.get_default_database()