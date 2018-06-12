#!/usr/local/var/pyenv/shims/python

import mongomock
import requests
from mockito import when, mock, unstub, mockito, patch
from pymongo import MongoClient
import sys
from securlet_sample_calls import *
from mock import patch
from requests import Response

from tests.test_box import stored_obj

sys.path.append('/Users/preethi_sundaravarad/elastica/mongoTutorial/tests/')


box_get_file_uri = 'https://api.box.com/2.0/files/295640148418'


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
    #mongo_update_age()
    for obj in objects:
        stored_obj = collection.find_one({'_id' : obj['_id']})
        stored_obj['age'] -= 1
        assert stored_obj == obj # by comparing all fields we make sure only votes changed

def mongo_update_mocker():
    collection = mongomock.MongoClient().db.collection
    objects = [dict(age=1), dict(age=2)]
    for obj in objects:
        obj['_id'] = collection.insert(obj)
    #mongo_update_age()
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

