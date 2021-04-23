import sys
import time

import requests as req
from config import POST_ID, TOKEN

url = f"https://graph.facebook.com/v10.0/{POST_ID}?fields=comments.limit(4000)%7Buser%2Cusername%7D&access_token={TOKEN}"

DATA = []


def get(next_url: str):
    global DATA
    r = req.get(next_url)
    r_json = r.json()
    data = r_json.get('data')
    if data:
        DATA = [*DATA, *data]
    try:
        f_next = r_json.get('paging').get('next')
        if f_next:
            get(f_next)
    except AttributeError:
        print("there is n\'t any other page")
        print("comments_count", len(DATA))
        counter()
        return
    return


def main():
    global DATA
    r_first = req.get(url)
    res_json = r_first.json()
    time.sleep(1)
    try:
        error = res_json.get('error').get('message')
        if error:
            print(error)
            sys.exit(0)
    except AttributeError:
        print('No error')
        pass
    data_first = r_first.json().get('comments').get('data')
    DATA = [*DATA, *data_first]
    get(res_json.get('comments').get('paging').get('next'))
    return


def counter():
    global DATA
    out = {}
    for i in DATA:
        if out.get(i.get('username')):
            out[i.get('username')] += 1
        else:
            out[i.get('username')] = 1

    sort_out = sorted(out.items(), key=lambda x: x[1], reverse=True)

    c = 0
    for i in sort_out:
        if c <= 10:
            print(i[0], i[1])
            c += 1
    return


if __name__ == '__main__':
    main()