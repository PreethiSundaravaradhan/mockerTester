import pymongo
from pymongo import MongoClient

def get_mongo_db():
    db = MongoClient().test
    return db


def print_mongo_users():
    db = get_mongo_db()
    usr = db.collab
    for user in usr.find():
        print(user)
    return usr


def get_mongo_users():
    db = get_mongo_db()
    usr = db.users
    return usr


def mongo_add(json):
   # client = MongoClient()
    db = get_mongo_db()
    x = db.collab.insert(json)
    return x

def mongo_delete_all():
    db = get_mongo_db()
    db.users.remove()
    return

if __name__ == "__main__":
    mongo_add({"collab": 1})

