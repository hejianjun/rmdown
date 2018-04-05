#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json,os,requests,progressbar,logging
from lxml import etree
from multiprocessing import Pool
#import pdb

max_thread_num = 4
json_file = 'YaZhouWuMa.jsonlines'
url = 'http://www.rmdown.com/download.php'
root_path ='E:\\torrent\\'

def load(json_file,callback):
    fsize = os.path.getsize(json_file)
    bar = progressbar.ProgressBar(max_value=fsize)
    p = Pool(max_thread_num)
    with open(json_file, 'r') as file:
        for line in file:
            #pdb.set_trace()
            try:
                data = json.loads(line)
                if data.has_key('t_title') and data.has_key('file_urls'):
                    folder = file_folder(data["t_title"])
                    logging.info(folder)
                    for file_url in data["file_urls"]:
                        payload = get_payload(file_url);
                        if payload.has_key('ref') and payload.has_key('reff'):
                            path = '%s/%s.torrent' % (folder,payload["ref"])
                            p.apply_async(callback,args=(path,payload))
            except Exception,e:
                logging.error(e)
            i=file.tell()
            bar.update(i)
    p.close()
    p.join()

def file_folder(title):
    if len(title):
        title = title[0]
        table = dict((ord(char), None) for char in "|\\?*<\":>+[]/'")
        title = title.translate(table)
    else:
        title = u'test'
    if not os.path.exists(root_path+title):
        os.makedirs(root_path+title)
    return title

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
    progressbar.streams.wrap_stderr()
    logging.basicConfig()
    load(json_file,download)