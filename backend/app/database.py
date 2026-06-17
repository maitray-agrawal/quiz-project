from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["edulens"]

students_col = db["students"]
assessments_col = db["assessments"]
interventions_col = db["interventions"]