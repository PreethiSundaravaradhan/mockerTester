#!/usr/local/var/pyenv/shims/python
import json

from mock import patch
from mongo_apis import get_mongo_collab

from securlet_sample_calls import process_one_event
from tests.test_box import mocked_mongo_insert, mocked_requests_get, mocked_requests_post, mocked_requests_delete
from tests.test_mongomocker import mocked_mongo_find


def mocked_download(self):
    # don't download, simply return true which means downloaded successfully
    return True


@patch('requests.delete', side_effect=mocked_requests_delete)
@patch('requests.post', side_effect=mocked_requests_post)
@patch('requests.get', side_effect=mocked_requests_get)
@patch('pymongo.collection.Collection.insert', side_effect=mocked_mongo_insert)
@patch('pymongo.collection.Collection.find', side_effect=mocked_mongo_find)
@patch('box_apis.box_api._download_file', side_effect=mocked_download)
def fake_UC1_tester(self, *args):
    file = './data/events/get_event_multiple.json'
    with open(file) as f:
        events = json.load(f)
    # events = json.loads(event_datapath+"/get_item_download.json")

    entries = events["entries"]

    for entry in entries:
        process_one_event(entry)

    # count_compliant from mongo
    records = get_mongo_collab('status', 'non-compliant')
    count_nonc = records.count()
    print(count_nonc)
    assert count_nonc == 1

if __name__ == '__main__':
    fake_UC1_tester()