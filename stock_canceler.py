# -*- coding: utf-8 -*-

import json
import os
import sys

import requests

def abort(msg):
    print('Error!: {0}'.format(msg))
    sys.exit(1)

def get(url, params, headers):
    r = requests.get(url, params=params, proxies=proxies, headers=headers)
    return r

def delete(url):
    r = requests.delete(url, proxies=proxies, headers=headers)
    return r

def print_response(r, title=''):
    c = r.status_code
    h = r.headers
    print('{0} Response={1}, Detail={2}'.format(title, c, h))

def assert_response(r, title=''):
    c = r.status_code
    h = r.headers
    if c<200 or c>299:
        abort('{0} Response={1}, Detail={2}'.format(title, c, h))

class Stock:
    def __init__(self, d):
        self.id     = d['id']
        self.title  = d['title']

def get_stocks(target_userid, page, per_page):
    url = 'https://qiita.com/api/v2/users/{}/stocks'.format(target_userid)
    params = {
        'page'     : page,
        'per_page' : per_page,
    }
    r = get(url, params, headers)

    items = r.json()
    stocks = []
    is_last = False

    # int(r.headers['Total-Count']) 見た方が良い?
    # でも len(items) と Total-Count が食い違うケースはそうはないと思う(思いたい)ので
    # とりあえず len で判定.
    if len(items) < per_page:
        is_last = True

    for i,item in enumerate(items):
        stock = Stock(item)
        stocks.append(stock)

    return [stocks, is_last]

def cancel_stock(item_id):
    url = 'https://qiita.com/api/v2/items/{}/stock'.format(item_id)
    r = delete(url)
    return r

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Qiita Stock Canceler.',
    )

    parser.add_argument('-u', '--username', default=None, required=True,
        help='Your Qiita Username.')

    parsed_args = parser.parse_args()
    return parsed_args

args = parse_arguments()

MYDIR = os.path.abspath(os.path.dirname(__file__))

proxies = {
    "http": os.getenv('HTTP_PROXY'),
    "https": os.getenv('HTTPS_PROXY'),
}
token = os.getenv('QIITA_ACCESS_TOKEN')
headers = {
    'content-type'  : 'application/json',
    'charset'       : 'utf-8',
    'Authorization' : 'Bearer {0}'.format(token)
}

# 1/2 Get all my stock ID
# -----------------------

PAGE_START_NO = 1
target_userid = args.username
per_page = 100

cur_page = PAGE_START_NO
all_stocks = []

while True:
    a = (cur_page-1)*per_page + PAGE_START_NO
    b = a + per_page - 1
    print('getting between {} to {}...'.format(a, b))

    stocks, is_last = get_stocks(target_userid, cur_page, per_page)
    all_stocks.extend(stocks)

    if is_last:
        break

    cur_page += 1

#for i,stock in enumerate(all_stocks):
#    print('{} ID:{}, {}'.format(i+1, stock.id, stock.title))

# 2/2 delete all stock
# --------------------

total_count = len(all_stocks)
for i,stock in enumerate(all_stocks):
    target_id = stock.id
    caption = '{}/{} TITLE:{}'.format(i+1, total_count, stock.title)

    print('{}...'.format(caption))
    r = cancel_stock(target_id)
    assert_response(r, title=caption)

print('Fin.')
