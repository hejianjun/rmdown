import time
import progressbar
import os
import logging

progressbar.streams.wrap_stderr()
logging.basicConfig()

json_file = 'YaZhouWuMa.jsonlines'

fsize = os.path.getsize(json_file)
bar = progressbar.ProgressBar(max_value=fsize)
file = open(json_file, 'r')
for line in file:
    time.sleep(0.001)
    i=file.tell()
    bar.update(i)