#!/usr/bin/env python

import json
import pandas as pd
from block_io import BlockIo
version = 2 # API version
block_io = BlockIo('a2dc-4fe6-5763-9d5f', 'Gold2020', version)

transactions = '../../notebooks/output/data_addresses'
addresses = []

df = pd.read_csv(transactions)

for index, row in df.iterrows():
    data = (block_io.get_address_balance(addresses=row['address']))
    data = data['data']['balances']
    data = data[0]
    address = data['address']
    available_balance = data['available_balance']
    pending_received_balance = data['pending_received_balance']
    print(address, available_balance, pending_received_balance)
    temp = {
        "address": address,
        "available_balance": available_balance,
        "pending_received_balance": pending_received_balance
    }
    addresses.append(temp)

print(len(addresses))

with open('output/wallet_stats.json', 'w') as jsonfile:
    json.dump(addresses, jsonfile, encoding='utf8')