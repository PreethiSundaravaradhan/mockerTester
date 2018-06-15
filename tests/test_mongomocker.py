#!/usr/local/var/pyenv/shims/python
import mongomock
from mockito import when, mock, unstub, mockito, patch
import sys
from box.securlet_sample_calls import *
from tests.test_box import stored_obj

sys.path.append('/Users/preethi_sundaravarad/elastica/mongoTutorial/box/')


box_get_file_uri = 'https://api.box.com/2.0/files/295640148418'


def mocked_mongo_find(condition):
    collection = mongomock.MongoClient().db.collab
    for item in stored_obj:
        collection.insert(item)
    return collection.find(condition)

def box_api_mocker(uri):
    response = mock({'status_code': 200, 'text': 'Ok'})
    when(requests).get(uri).thenReturn(response)
    requests.get(uri)
    unstub()

def tmongo_update():
    collection = mongomock.Connection().db.collection
    objects = [dict(age=1), dict(age=2)]
    for obj in objects:
        obj['_id'] = collection.insert(obj)
    for obj in objects:
        stored_obj = collection.find_one({'_id' : obj['_id']})
        stored_obj['age'] -= 1
        assert stored_obj == obj # by comparing all fields we make sure only votes changed

def mongo_update_mocker():
    collection = mongomock.MongoClient().db.collection
    objects = [dict(age=1), dict(age=2)]
    for obj in objects:
        obj['_id'] = collection.insert(obj)
    for obj in objects:
        stored_obj = collection.find_one({'_id' : obj['_id']})
        stored_obj['age'] -= 1
        assert stored_obj == obj # by comparing all fields we make sure only votes changed

def es_update():
    print("some actual es calls")
    return

def mocked_mongo_conn(self, database = 'test'):
    print("mocking - mongo ---- $$$$$$")
    return mongomock.MongoClient().db.test

