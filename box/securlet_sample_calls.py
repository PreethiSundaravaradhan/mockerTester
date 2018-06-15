#!/usr/local/var/pyenv/shims/python
import json
import requests
import requests.auth

from box_apis import box_api
from mongo_apis import mongo_collab_add, get_mongo_users
from stream_processing import get_event


def mongo_add_person(item_id, item_type, user_id, json):
    #person = {'name': name,'age':1,'status': 'pending'}
    #x = mongo_collab_add(person)
    usr = get_mongo_users()
    #print("mongo after adding -->" + str(x))
    cursor = usr.find({"user_id": user_id})
    for document in cursor:
        if(document['item_id'] == item_id):
            json["user_id"] = user_id
            json["item_id"] = item_id
            json["item_type"] = item_type
            usr.update(document, json)
    return usr


def mongo_add_json(data):
    x = mongo_collab_add(data)
    # usr = get_mongo_users()
    return x


def es_get_person(name):
    es_loc = 'http://localhost:9200/accounts/person/_search?q='+name
    response = requests.get(es_loc)
    print("\nelastic search true call -->")
    es = json.loads(response._content)
    print(es)
    if(es['hits']['total'] == 0):
        return None
    return es['hits']['hits']


def process_one_event(event_json):
    box_client = box_api(token)
    et = event_json["event_type"]
    types = et.split("_")
    if types[0] == 'ITEM':
        print("type 1 events : " + et)
        if event_json["source"]["type"] == 'file':
            file_id = event_json["source"]["id"]
            if download_file(box_client, file_id):
                inspect_content(file_id, event_json["source"]["name"])
            else:
                print("unable to download.. unexpected error")
    elif types[0] == 'COLLAB':
        print("type 2 events : " + et)
        collabs = find_collabs(box_client, event_json["source"])
        for c in collabs:
            item_id = c["item"]["id"]
            item_type = c["item"]["type"]
            mongo_add_person(item_id, item_type, c["accessible_by"]["id"], c)

    return


def remove_blacklist_users(box_client, collab_id):
    # remove collabs
    status = box_client._remove_collab(collab_id)
    if status == 204:
        report_finds(collab_id, "blacklisted")
        return True
    return False

def download_file(box_client, file_id):
    r = box_client._download_file(file_id)
    return r

def find_collabs(box_client, source):
    collab_id = source["id"]
    collab_details = box_client._get_collab_by_id(collab_id)
    if source['role'] == 'editor' or '+' in source['accessible_by']['login']:
        if(remove_blacklist_users(box_client, source["id"])):
            item_type = source["item"]["type"]
            item_id = source["item"]["id"]
            all_collabs = box_client._collab_one_file(item_id, item_type)
            return all_collabs["entries"]
    return collab_details["entries"]

def inspect_content(file_id, file_name):
    if ".txt" in file_name:
        with open("../tests/data/files/"+file_id, "r") as ins_file:
            lines = ins_file.readlines()
            for line in lines:
                if "VISA" in line:
                    return report_finds(file_id)
    return None


def report_finds(file_id, status=None):
    if status is None:
        json = {"status": "non-compliant", "file_id": file_id}
    else:
        json = {"status": status, "file_id": file_id}
    mongo_collab_add(json)
    return


def fetch_events():
    uri = 'https://api.box.com/2.0/events'
    header = {'Authorization': 'Bearer ' + token}
    params = {'limit': 20}
    events = get_event(uri, header, stream_position=None, etype=None)
    return events["entries"]


def collab_files_on_folder(token, parent_0, user_q):

    box = box_api(token)

    # box create folder/subfolders and some random files
    folder_id = box._folder_create("somefolder8", parent_0)
    box._file_upload(folder_id, "textfile.txt")
    uploaded_f_id3 = box._folder_create("somefolder2_l3", folder_id)

    # get all subfolder in parent
    all_folders = box._get_folder_entries(folder_id)

    # get collab for uploaded_f_id3
    # add to mongo
    collabfid3 = box._collab_one_file(uploaded_f_id3)
    parent_collab = box._collab_one_file(folder_id)
    mongo_collab_add(collabfid3)

    for entry in collabfid3['entries']:
        if entry['accessible_by']['login'] == user_q:
            user_id = entry['accessible_by']['id']
            del_status = box._remove_collab(entry['id'])
            print("delete status == " + str(del_status))

    all_folders_ad = box._get_folder_entries(folder_id)
    new_parent_collab = box._collab_one_file(folder_id)
    count = 0
    for entry in all_folders:
        for collab_old in parent_collab["entries"]:
            found = 0
            for collab_new in new_parent_collab["entries"]:
                if collab_old['accessible_by']['login'] == collab_new['accessible_by']['login']:
                    found = 1
            if found == 0:
                ++count
                box._collab_post(entry["item"]["id"], user_id)

    mongo_add_person(user_q)

    # some mongo call
    mongo_add_person(parent_collab["entries"][0]['accessible_by']['name'])

    # es call
    es_person = es_get_person(user_q)

    print('\nother logic true responses --> ')
    # 'other calls'
    if (es_person is None):
        print('none')
    else:
        print(es_person)

    return count

def func_sample():
    box_get_file_uri = 'https://api.box.com/2.0/files/285571189078'
    box_dev_token = 'VdU3PWHbKXfx4r3AOvX2mcwrGXAOJZsx'
    # box_token = box_oauth2()

    box = box_api(box_dev_token)
    # box call
    box_file_owner = box._get_one_file('295987792281')

    # some mongo call
    p_name = box_file_owner
    # print(p_name)
    mongo_add_person(p_name)

    # es call
    es_person = es_get_person(box_file_owner)

    print('\nother logic true responses --> ')
    # 'other calls'
    if(es_person is None):
        print('none')
    else:
        print(es_person)

    return

def demo_case1():
    events = fetch_events()
    for event in events:
        process_one_event(event)
    return

if __name__ == "__main__":
    token = '6YkNMx7FwXQU0wDkGID7QswsAssrFrKC'
    parent_0 = '50218147730'
    user_q = 'Preethi_Sundaravarad@symantec.com'
    demo_case1()

dicti = []
token = '6YkNMx7FwXQU0wDkGID7QswsAssrFrKC'