from pymongo import MongoClient

db_client = MongoClient("mongodb://localhost:27017")
db = db_client.db_portfolio
users_collection = db.users
projects_collection = db.projects