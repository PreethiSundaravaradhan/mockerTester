#!/usr/local/var/pyenv/shims/python
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

def get_mongo_collab(key, val):
    db = get_mongo_db()
    x = db.collab.find({key:val})
    return x

def get_mongo_users():
    db = get_mongo_db()
    usr = db.users
    return usr


def mongo_collab_add(json):
   # client = MongoClient()
    db = get_mongo_db()
    x = db.collab.insert(json)
    return x

def mongo_file_info_add(json):
    db = get_mongo_db()
    x = db.fileinfo.insert(json)
    return x

def mongo_delete_all():
    db = get_mongo_db()
    db.users.remove()
    return

def mongo_events_add(json):
    db = MongoClient().elastica
    x = db.events.insert(json)
    return x

if __name__ == "__main__":
    mongo_collab_add({"collab": 1})

