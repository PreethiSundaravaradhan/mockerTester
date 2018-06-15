import json
from pprint import pprint
from random import randint

import requests

class box_api:
    def __init__(self, token):
        self.uri_domain = 'https://api.box.com/2.0/'
        self.header = {'Authorization': 'Bearer ' + token}

    def _get_folder_entries(self, folder_id):
        uri = self.uri_domain + 'folders/' + folder_id
        response = requests.get(uri, headers=self.header)
        file_meta = json.loads(response.text)
        return file_meta['item_collection']['entries']

    def _get_one_file(self, file_id):
        uri = self.uri_domain + 'files/' + file_id
        response = requests.get(uri, headers=self.header)
        file_meta = json.loads(response.text)
        owner = file_meta['owned_by']['name']
        print("\nbox api true response -->\n" +response.text)
        return owner

    def _download_file(self, file_id):
        uri = self.uri_domain + 'files/' + file_id + '/content'
        response = requests.get(uri, headers=self.header, stream=True)
        print(response.status_code)
        local_filename = uri.split('/')[-2]
        local_filename = "./tests/data/files/"+local_filename
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        if response.status_code == 200:
            return True
        return False

    def _get_collab_by_id(self, _id):
        uri = self.uri_domain + 'collaborations/' + _id
        response = requests.get(uri, headers=self.header)
        file_meta = json.loads(response._content)
        print(json.dumps(file_meta, indent=2))
        return file_meta

    def _collab_one_file(self, _id, type = 'folders'):
        uri = self.uri_domain + type + '/' + _id + '/collaborations'
        response = requests.get(uri, headers=self.header)
        file_meta = json.loads(response.text)
        print(json.dumps(file_meta, indent=2))
        return file_meta

    def _event_get(self):
        uri = self.uri_domain + 'events'
        response = requests.get(uri, headers=self.header)
        file_meta = json.loads(response._content)
        print(json.dumps(file_meta, indent=2))
        return

    def _folder_create(self, folder_name, parent=None):
        req_uri = self.uri_domain + 'folders'
        req_file = '../tests/data/folders/_post.json'
        with open(req_file) as f:
            d = json.load(f)
        d["name"] = folder_name
        if parent is not None:
            d["parent"]["id"] = parent
        pprint(d)
        resp = requests.post(req_uri, headers=self.header, data=json.dumps(d))
        file_meta = json.loads(resp._content)
        print(json.dumps(file_meta, indent=2))
        id = file_meta['id']
        return id

    def _collab_post(self, item_id, user_id):
        req_uri = self.uri_domain + 'collaborations/'
        req_file = '../tests/data/collaborations/_post_file.json'
        with open(req_file) as f:
            data = json.load(f)
        data['item']['id'] = item_id
        data['accessible']['by'] = user_id
        pprint(data)
        resp = requests.post(req_uri, headers=self.header, data=data)
        file_meta = json.loads(resp.text)
        print(json.dumps(file_meta, indent=2))
        return

    def _file_upload2(self, folder_id):
        req_uri = 'https://upload.box.com/api/2.0/files/content'
        req_file = '../tests/data/files/_upload.json'
        with open(req_file) as f:
            data = json.load(f, encoding='UTF-8')
            data["parent"]["id"] = folder_id
            data["name"] = "file8.txt"
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; " \
                  "name=\"attributes\"\r\n\r\n" + json.dumps(data) +\
                  "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"file\"; " \
                  "filename=\"open(\"../tests/data/files/textfile.txt\")\"\r\nContent-Type: text/plain\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
                  #"filename=\"dummy.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        h = self.header['Authorization']
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Authorization': h,
            'Cache-Control': "no-cache"
        }

        response = requests.request("POST", req_uri, data=payload, headers=headers)
        print(response.text)
        return

    def _file_upload(self, folder_id, file_name):
        req_uri = 'https://upload.box.com/api/2.0/files/content'
        req_file = './tests/data/files/_upload.json'
        #self.header['content-type'] = "multipart/form-data; boundary=--9ab71612ef814caa943de28bc9d0f830"
        with open(req_file) as f:
            data = json.load(f, encoding='UTF-8')
        data["parent"]["id"] = folder_id
        data["name"] = 'textfile'+str(randint(0, 10000000000))+'.txt'
        print(json.dumps(data))

        multipart_form_data = {
            "file": ('custom_file_name.txt', open('../tests/data/files/'+file_name, 'rb'), 'text/plain')}
        d = {"attributes" : json.dumps(data)}
        resp = requests.post(req_uri, headers=self.header, files=multipart_form_data, data = d)
        #resp = requests.post(req_uri, headers=self.header, data=data, files = )
        print(resp.status_code)
        file_meta = json.loads(resp.text)
        print(json.dumps(file_meta, indent=2))
        file_id = file_meta["entries"][0]["id"]
        return file_id


    def _remove_collab(self, collab_id):
        req_uri = self.uri_domain + 'collaborations/'
        req_uri = req_uri+collab_id
        print(req_uri)
        response = requests.delete(req_uri, headers = self.header)
        print(response.status_code)
        return response.status_code


if __name__ == '__main__':
    token = 'tw3UyK7fq2JQyBkCNdgjOc0yoDILWZVw'
    box = box_api(token)
    # folder_id = box._collab_one_file('50227983450')
    #data = box._get_collab_by_id('13450383417')
    #x = box._remove_collab('13450383417')
    #print(x)

    box._download_file(str(297549297696))
    #box._collab_post()
    #folder_id = box._file_upload2(50218147730)#
    #folder_id = box._file_upload(50218147730, 'textfile.txt')
#    print("returned = "+folder_id)
    #valu = box._event_get()