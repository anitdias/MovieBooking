from pymongo import MongoClient
from scripts.constants.app_constanst import Constants

mongo_uri = Constants.mongo_uri
database_name = Constants.db

client = MongoClient(mongo_uri)

db = client[database_name]
