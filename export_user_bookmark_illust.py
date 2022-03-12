import json
import time

from pixivpy3 import *

with open('config.json') as f:
    conf = json.load(f)

api = AppPixivAPI()
api.auth(refresh_token=conf['token'])

page = int(1)

illusts = []

res = api.user_bookmarks_illust(user_id=conf['user_id'])
for il in res.illusts:
    with open('bookmark.list', 'a', encoding='utf-8') as f:
        f.write(str(il.id) + '\n')


while True:
    time.sleep(5)
    page += 1
    qs = api.parse_qs(res.next_url)
    res = api.user_bookmarks_illust(**qs)
    if 'illusts' not in res:
        print('Error in page ' + str(page))
        print(res)
        continue
    for il in res.illusts:
        with open('bookmark.list', 'a', encoding='utf-8') as f:
            f.write(str(il.id) + '\n')
