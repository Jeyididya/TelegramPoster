from decouple import Config, RepositoryEnv
from pymongo import MongoClient


config = Config(RepositoryEnv('.env'))

db_pass = config('DB_PWD')

# connection_string = f"mongodb+srv://poster_admin:{db_pass}@cluster0.zc1qf6e.mongodb.net/?retryWrites=true&w=majority"

# # mongodb+srv://poster_admin:EReaDf5cFhQqc9x@cluster0.zc1qf6e.mongodb.net/

# client = MongoClient(connection_string)

# dbs = client.list_database_names()

# databse = client.instaPic
# personal_collection = databse.personal
# collections = databse.list_collection_names()
# print(collections)


# def insert_data(data):
#     personal_collection.insert_one(data)


# def search_data(data=""):
#     people = personal_collection.find(data)
#     for i in people:
#         print(i)


# search_data()


class DATABASE:
    def __init__(self):
        self.connection_string = f"mongodb+srv://poster_admin:{db_pass}@cluster0.zc1qf6e.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.connection_string)
        self.database = self.client.instaPic
        self.users_collection = self.database.users

    def connect(self):
        pass

    def add_data(self, data):
        self.users_collection.insert_one(data)

    def get_data(self, data=""):
        users = self.users_collection.find(data)
        return list(users)


# db = DATABASE()

# print(db.get_data({"username": "eer"}))
