import json
import csv
import os
import time
from pathlib import Path

from pixivpy3 import *

with open('config.json') as f:
    conf = json.load(f)

api = AppPixivAPI()
api.auth(refresh_token=conf['token'])


with open('list-novel.csv') as f:
    for row in csv.reader(f):
        if (row[0].isdecimal() != True):
            continue

        id = int(row[0])

        if (os.path.exists('data/rawnovelmeta/' + row[0] + '.json')):
            continue

        metadata = api.novel_detail(id)

        if 'error' in metadata:
            time.sleep(5)
            continue

        print(id)

        dir = 'data/novel/' + str(metadata.novel.user.id) + '/'

        Path(dir).mkdir(parents=True, exist_ok=True)

        with open(dir + row[0] + '.json', 'w') as jf:
            json.dump(api.novel_text(id), jf)

        with open('data/rawnovelmeta/' + row[0] + '.json', 'w') as jf:
            json.dump(metadata, jf)

        time.sleep(5)
