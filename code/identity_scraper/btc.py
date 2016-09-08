
# https://chain.api.btc.com/v3/address/15urYnyeJe3gwbGJ74wcX89Tz7ZtsFDVew/

import json
import pandas as pd
import requests


transactions = '../../notebooks/output/data_addresses'
addresses = []

df = pd.read_csv(transactions)

for index, row in df.iterrows():

    r = requests.get('https://chain.api.btc.com/v3/address/' + row['address'])
    response = r.json()

    address = response['data']['address']
    received = response['data']['received']
    sent = response['data']['sent']
    balance = response['data']['balance']
    tx_count = response['data']['tx_count']
    unconfirmed_tx_count = response['data']['unconfirmed_tx_count']
    unconfirmed_received = response['data']['unconfirmed_received']
    unconfirmed_sent = response['data']['unconfirmed_sent']
    unspent_tx_count = response['data']['unspent_tx_count']
    temp = {
        "address": address,
        "received": received,
        "sent": sent,
        "balance": balance,
        "tx_count": tx_count,
        "unspent_tx_count": unspent_tx_count,
        "unconfirmed_tx_count": unconfirmed_tx_count,
        "unconfirmed_received": unconfirmed_received,
        "unconfirmed_sent": unconfirmed_sent
    }
    addresses.append(temp)

print(len(addresses))

with open('output/cypher_stats.json', 'w') as jsonfile:
    json.dump(addresses, jsonfile, encoding='utf8')