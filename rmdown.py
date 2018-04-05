import json
import requests
from lxml import etree
import os
import progressbar
import logging

json_file = 'YaZhouWuMa.jsonlines'
url = 'http://www.rmdown.com/download.php'
root_path ='E:\\images\\'

def load(json_file,callback):
    bar = progressbar.ProgressBar()
    for line in bar(open(json_file, 'r')):
        data = json.loads(line)
        if data.has_key('t_title') and data.has_key('file_urls'):
            for file_url in data["file_urls"]:
                payload = get_payload(file_url);
                if payload.has_key('ref') and payload.has_key('reff'):
                    path=file_path(data["t_title"],payload["ref"])
                    callback(path,payload)

def file_path(title,ref):
    if len(title):
        title = title[0]
        table = dict((ord(char), None) for char in "|\\?*<\":>+[]/'")
        title = title.translate(table)
    else:
        title = u'ttt'
    if not os.path.exists(root_path+title):
        os.makedirs(root_path+title)
    logging.error('Got %d', title)
    return '%s/%s.torrent' % (title,ref)

def get_payload(url):
    r = requests.get(url)
    selector = etree.HTML(r.text)
    result = selector.xpath('//input')
    dict = {}
    for input in result:
        dict[input.get("name")]=input.get("value")
    return dict

def download(path,payload):
    r = requests.get(url,payload)
    with open(root_path+path, "wb") as decode:
        decode.write(r.content)

if __name__ == '__main__':
    load(json_file,download)