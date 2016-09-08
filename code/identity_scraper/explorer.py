#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import json
import re
import pandas as pd

addresses = []

# wallet_links = open('data/wallet.csv')
# wallet_links = csv.reader(wallet_links)

df = pd.read_csv('data/wallet.csv')
df = df[['Old/Historic_link', 'Gambling_link', 'Services_link', 'Pools_link', 'Exchanges_link']]
df_gambling = df['Gambling_link']
df_services = df['Services_link']
df_pools = df['Pools_link']
df_exchanges = df['Exchanges_link']
df_gambling = df_gambling.dropna()
df_services = df_services.dropna()
df_pools = df_pools.dropna()
df_exchanges = df_exchanges.dropna()

df_gambling = pd.DataFrame(df_gambling)
df_services = pd.DataFrame(df_services)
df_pools = pd.DataFrame(df_pools)
df_exchanges = pd.DataFrame(df_exchanges)

df_gambling.columns = ['link']
df_services.columns = ['link']
df_pools.columns = ['link']
df_exchanges.columns = ['link']

def lets_get_scraping(stem, id, num):
    for i in range(1, num):
        url = stem
        url = url + '/addresses?page={0}'.format(i)
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            for tr in soup.table.find_all('tr'):
                if tr:
                    for td in tr.find_all('td'):
                        if td:
                            for a in td.find_all('a'):
                                if a:
                                    if id == 1:
                                        temp = {a.get_text(): 1}
                                        addresses.append(temp)
                                    elif id == 6:
                                        temp = {a.get_text(): 6}
                                        addresses.append(temp)
                                    elif id == 3:
                                        temp = {a.get_text(): 3}
                                        addresses.append(temp)
                                    elif id == 4:
                                        temp = {a.get_text(): 4}
                                        addresses.append(temp)
                else:
                    print('error')
        except:
            print('error')
    return addresses


for index, row in df_gambling.iterrows():
    temp = row['link']
    r = requests.get(temp)
    soup = BeautifulSoup(r.text, 'html.parser')
    for foo in soup.find_all('div', attrs={'class': 'paging'}):
        num = foo.text
    pages = re.search('(?<=/\s)\d+', num).group(0)
    lets_get_scraping(row['link'], id=1, num=int(pages))

print('Completed: Gambling')

for index, row in df_services.iterrows():
    temp = row['link']
    r = requests.get(temp)
    soup = BeautifulSoup(r.text, 'html.parser')
    for foo in soup.find_all('div', attrs={'class': 'paging'}):
        num = foo.text
    pages = re.search('(?<=/\s)\d+', num).group(0)

    lets_get_scraping(row['link'], id=4, num=int(pages))

print('Completed: Services')

for index, row in df_pools.iterrows():
    temp = row['link']
    r = requests.get(temp)
    soup = BeautifulSoup(r.text, 'html.parser')
    for foo in soup.find_all('div', attrs={'class': 'paging'}):
        num = foo.text
    pages = re.search('(?<=/\s)\d+', num).group(0)

    lets_get_scraping(row['link'], id=6, num=int(pages))

print('Completed: Pools')

for index, row in df_exchanges.iterrows():
    temp = row['link']
    r = requests.get(temp)
    soup = BeautifulSoup(r.text, 'html.parser')
    for foo in soup.find_all('div', attrs={'class': 'paging'}):
        num = foo.text
    pages = re.search('(?<=/\s)\d+', num).group(0)

    lets_get_scraping(row['link'], id=3, num=int(pages))

print('Completed: Exchanges')

print(addresses)
print(len(addresses))

with open('output/pools.json', 'w') as jsonfile:
    json.dump(addresses, jsonfile, encoding='utf8')
