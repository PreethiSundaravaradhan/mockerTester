import mongomock
import requests
#import requests_oauthlib
from mockito import when, mock, unstub, mockito, patch
from pymongo import MongoClient
import sys
from securlet_sample_calls import *
from mock import patch
from requests import Response

sys.path.append('/Users/preethi_sundaravarad/elastica/mongoTutorial/home/')


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

def mocked_mongo_conn(self):
    print("mocking- mongo ----$$$$$$")
    return mongomock.Connection()

def mocked_mongo_insert(json):
    json['mocked'] = 'true'
    collection = mongomock.MongoClient().db.test
    collection.insert(json)
    return collection


def mocked_requests_get(value, headers = 'token'):
    print("current uri =="+value)
    expected_resp = Response()
    if(value == 'https://api.box.com/2.0/files/295640148418'):

        dict =  {"type": "file", "id": "295640148418", "file_version": {"type": "file_version", "id": "311221311010","sha1": "92c9614354519c993b8b52a2a1da4e2d078dca89"},"sequence_id": "0", "etag": "0", "sha1": "92c9614354519c993b8b52a2a1da4e2d078dca89",
         "name": "Welcome to Box.pdf", "description": "", "size": 5206506, "path_collection": {"total_count": 1, "entries": [{"type": "folder",
                                                                                                    "id": "0",
                                                                                                    "sequence_id": 'null',
                                                                                                    "etag": 'null',
                                                                                                    "name": "All Files"}]},
         "created_at": "2018-06-01T16:41:14-07:00", "modified_at": "2018-06-01T16:41:14-07:00", "trashed_at": 'null',
         "purged_at": 'null', "content_created_at": "2017-08-21T16:46:48-07:00",
         "content_modified_at": "2017-08-21T16:46:48-07:00",
         "created_by": {"type": "user", "id": "3691026112", "name": "Mocked User",
                        "login": "preethisundarv@gmail.com"},
         "modified_by": {"type": "user", "id": "3691026112", "name": "Mocked User",
                         "login": "preethisundarv@gmail.com"},
         "owned_by": {"type": "user", "id": "3691026112", "name": "Mocked User",
                      "login": "preethisundarv@gmail.com"}, "shared_link": 'null',
         "parent": {"type": "folder", "id": "0", "sequence_id": 'null', "etag": 'null', "name": "All Files"},
         "item_status": "active"}
        expected_resp._content = json.dumps(dict)
        print("###here returned")
        return expected_resp
    elif(value == 'http://localhost:9200/accounts/person/_search?q=Mocked User'):
        dict = {"took":1,"timed_out":'false',"_shards":{"total":5,"successful":5,"skipped":0,"failed":0},"hits":{"total":1,"max_score":0.2876821,"hits":[{"_index":"accounts","_type":"person","_id":"5","_score":0.2876821,"_source":{
                "name" : "Mocked","age" : "5","status" : "done"}}]}}
        expected_resp._content = json.dumps(dict)
        return expected_resp

    else:
        print("not equal!!!!!!!!!!!"+value)
    return "error"


@patch('pymongo.MongoClient', side_effect=mocked_mongo_conn)
@patch('requests.get', side_effect=mocked_requests_get)
@patch('pymongo.collection.Collection.insert', side_effect=mocked_mongo_insert)
def test_func_sample(self, *args):
    func_sample()


test_func_sample()