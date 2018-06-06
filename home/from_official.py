import pymongo
from pymongo import MongoClient

def get_mongo_db():
    db = MongoClient().test
    return db


def print_mongo_users():
    db = get_mongo_db()
    usr = db.users
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
    db.users.insert(json)
    return

def mongo_delete_all():
    db = get_mongo_db()
    db.users.remove()
    return

print_mongo_users()

