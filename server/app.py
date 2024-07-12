import json
from pymongo import MongoClient

DB_NAME = "digital_music_library"
DB_COL_NAME = "data"

client = MongoClient("mongodb://localhost:27017/") # connect to MongoDB server

# Loading the data from the JSON file will be done only once.
# In MongoDB a database and a collection are not created unless
# content is added. Since we have to add the content once, we
# will check if the database and the collection exist and in
# case they don't, we will import the contents from the JSON file

db = client[DB_NAME] # create database
mongo_db_list = client.list_database_names()
if DB_NAME not in mongo_db_list:
    db_data = db[DB_COL_NAME] # create collection for the database to store data
    db_col_list = db.list_collection_names()

    if DB_COL_NAME not in db_col_list:
        # load the JSON file in the database collection
        with open('../data.json') as file:
            file_data = json.load(file)

        if isinstance(file_data, list):
            db_data.insert_many(file_data) # use insert_many in case the file contains more than one entry
        else:
            db_data.insert_one(file_data)

        print(f"JSON file imported successfully to collection {DB_COL_NAME} in database {DB_NAME}!")
    else:
        print(f"Collection with {DB_COL_NAME} already exists.")
else:
    print(f"Database with {DB_NAME} already exists.")

