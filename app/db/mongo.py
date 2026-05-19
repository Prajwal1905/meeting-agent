from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["meeting_agent"]

meetings_collection = db["meetings"]