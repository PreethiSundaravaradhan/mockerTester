from copy import deepcopy

import mongomock
import requests
from mockito import when, mock, unstub, mockito, patch
from pymongo import MongoClient
import sys
from securlet_sample_calls import *
from mock import patch
from requests import Response

sys.path.append('/Users/preethi_sundaravarad/elastica/mongoTutorial/tests/')
box_get_file_uri = 'https://api.box.com/2.0/files/295640148418'

box_uri_identifier = "box.com"
es_uri_identifier = "accounts/person"



def mocked_mongo_insert(json):
    json['mocked'] = 'true'
    collection = mongomock.MongoClient().db.test
    collection.insert(json)
    for ob in collection.find():
        stored_obj.append(ob)
    print(stored_obj)

# Process each of file, folder, collab differently
def mocked_box_get_apis(value, stream):
    req_file = './data/collaborations/_get_file.json'
    parsed_url = value.split("/")
    item = parsed_url[4]
    if(item == 'files'):
        if len(parsed_url) > 6:
            if(parsed_url[6] == 'collaborations'):
                req_file = './data/collaborations/_get_file.json'
            elif((parsed_url[6] == 'content') and (stream == True)):
                req_file = './data/files/textfile.txt'
                # with open(req_file) as file:
                return req_file

        else:
            req_file = './data/files/_get.json'

    if(item == 'folders'):
        if len(parsed_url) > 6:
            if (parsed_url[6] == 'collaborations'):
                req_file = './data/collaborations/_get_folder.json'
        else:
            req_file = './data/folders/_get.json'

    with open(req_file) as f:
        d = json.load(f)

    return json.dumps(d)


# Isolates box, es, mongo and other calls based on post request uri
def mocked_box_post_apis(value, data=None, headers = 'token', files=None):
    req_file = './data/collaborations/_get_file.json'
    parsed_url = value.split("/")
    item = parsed_url[4]
    if (item == 'files'):
        if len(parsed_url) > 6:
            if parsed_url[6] == 'collaborations':
                req_file = './data/collaborations/_get_file.json'
        else:
            req_file = './data/files/response/_post.json'

    if (item == 'folders'):
        if len(parsed_url) > 6:
            if parsed_url[6] == 'collaborations':
                req_file = './data/collaborations/_get_folder.json'
        else:
            req_file = './data/folders/response/_post.json'

    with open(req_file) as f:
        d = json.load(f)

    return json.dumps(d)


def mocked_requests_delete(value, data=None, headers='token', testcase='success'):
    expected_resp = Response()
    if testcase == 'success':
        expected_resp.status_code = 204
    else:
        expected_resp.status_code = 401
    return expected_resp


def mocked_requests_post(value, data, headers = 'token', files=None, testcase='success'):
    expected_resp = Response()
    if box_uri_identifier in value:  # example: 'https://api.box.com/2.0/files/295640148418'):
        mock_file = mocked_box_post_apis(value)
        expected_resp._content = mock_file
        return expected_resp

    elif es_uri_identifier in value:
        file_uri = "./data/es/_get_person.json"
        with open(file_uri) as f:
            d = json.load(f)

        expected_resp._content = json.dumps(d)
        return expected_resp

    else:
        print("Handle this URI correctly: " + value)
    return "error"


def generate_file(file):

    return

# Isolates box, es, mongo and other calls based on get request uri
def mocked_requests_get(value, headers = 'token', testcase='success', stream=False):
    expected_resp = Response()
    if box_uri_identifier in value:  # example: 'https://api.box.com/2.0/files/295640148418'):
        mock_file = mocked_box_get_apis(value, stream)
        if(stream == True):
            with open(mock_file) as file1:
                expected_resp._content = file1.read()
                expected_resp.iter_content = generate_file(file1)
        else:
            expected_resp._content = mock_file
        return expected_resp

    elif es_uri_identifier in value:
        file_uri = "./data/es/_get_person.json"
        with open(file_uri) as f:
            d = json.load(f)

        expected_resp._content = json.dumps(d)
        return expected_resp

    else:
        print("Handle this URI correctly: " + value)
    return "error"


# Todo::collab_files_on_folder mockers

# @patch('pymongo.database.Database', side_effect=mocked_mongo_conn)
@patch('requests.delete', side_effect=mocked_requests_delete)
@patch('requests.post', side_effect=mocked_requests_post)
@patch('requests.get', side_effect=mocked_requests_get)
@patch('pymongo.collection.Collection.insert', side_effect=mocked_mongo_insert)
def main_tester(self, *args):
    token = 'mycustomtoken123'
    parent_0 = '50218147730'
    user_q = 'Preethi_Sundaravarad@symantec.com'
    collab_files_on_folder(token, parent_0, user_q)
    # print(stored_obj)

stored_obj = []
# main_tester()