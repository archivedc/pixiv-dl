import json
import csv
import os
import time
from pathlib import Path

from pixivpy3 import *

api = AppPixivAPI()
api.auth(refresh_token=conf['token'])


with open('list.csv') as f:
    for row in csv.reader(f):
        if (row[0].isdecimal() != True):
            continue

        id = int(row[0])

        if (os.path.exists('data/rawmeta/' + row[0] + '.json')):
            continue

        metadata = None

        if (len(row) > 1 and row[1] == 'novel'):
            metadata = api.novel_detail(id)
        else:
            metadata = api.illust_detail(id)

        if 'error' in metadata:
            continue

        print(id)

        dir = 'data/img/' + str(metadata.illust.user.id) + \
            '/' + str(metadata.illust.id) + '/'

        Path(dir).mkdir(parents=True, exist_ok=True)

        if (metadata.illust.type == 'illust' or metadata.illust.type == 'manga'):
            if metadata.illust.page_count == 1:
                api.download(
                    metadata.illust.meta_single_page.original_image_url, dir)
            else:
                for page in metadata.illust.meta_pages:
                    api.download(page.image_urls.original,
                                 dir)
                    time.sleep(1)
        elif metadata.illust.type == "ugoira":
            ugoira_url = metadata.illust.meta_single_page.original_image_url.rsplit(
                '0', 1)
            ugoira = api.ugoira_metadata(id)
            ugoira_frames = len(ugoira.ugoira_metadata.frames)

            for frame in range(ugoira_frames):
                frame_url = ugoira_url[0] + str(frame) + ugoira_url[1]
                api.download(frame_url, path=dir)
                time.sleep(1)

        with open('data/rawmeta/' + row[0] + '.json', 'w') as jf:
            json.dump(metadata, jf)

        time.sleep(5)
