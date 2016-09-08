#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import json

addresses = []

def lets_get_scraping(url, id):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for tr in soup.tbody.find_all('tr'):
        for strong_tag in tr.find_all('strong'):
            if id == 1:
                temp = {strong_tag.get_text(): 1}
                addresses.append(temp)
            elif id == 2:
                temp = {strong_tag.get_text(): 2}
                addresses.append(temp)
            elif id == 3:
                temp = {strong_tag.get_text(): 3}
                addresses.append(temp)
            elif id == 4:
                temp = {strong_tag.get_text(): 4}
                addresses.append(temp)
    return addresses


for i in range(17):
    gambling = 'http://bitcoinwhoswho.com/search/index/index/keyword/gambling/page/{0}'.format(i)
    lets_get_scraping(gambling, id=1)

print('Completed: Gambling')

for i in range(2):
    charity = 'http://bitcoinwhoswho.com/search/index/index/keyword/charity/page/{0}'.format(i)
    lets_get_scraping(charity, id=2)

for i in range(34):
    charity = 'http://bitcoinwhoswho.com/search/index/index/keyword/donate/page/{0}'.format(i)
    lets_get_scraping(charity, id=2)

print('Completed: Charity')

for i in range(17):
    finance = 'http://bitcoinwhoswho.com/search/index/index/keyword/finance/page/{0}'.format(i)
    lets_get_scraping(finance, id=3)

print('Completed: Finance')

for i in range(162):
    exchange = 'http://bitcoinwhoswho.com/search/index/index/keyword/exchange/page/{0}'.format(i)
    lets_get_scraping(exchange, id=3)

print('Completed: Exchanges')

print(len(addresses))

with open('output/whoiswho.json', 'w') as jsonfile:
    json.dump(addresses, jsonfile, encoding='utf8')
