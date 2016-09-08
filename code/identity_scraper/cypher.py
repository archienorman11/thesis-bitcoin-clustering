#!/usr/bin/env python

import json
import pandas as pd
from blockcypher import get_address_overview


transactions = '../../notebooks/output/data_addresses'
addresses = []

df = pd.read_csv(transactions)

for index, row in df.iterrows():
    # print(get_address_overview('1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD'))
    data = (get_address_overview(row['address']))
    final_n_tx = data['final_n_tx']
    n_tx = data['n_tx']
    unconfirmed_balance = data['unconfirmed_balance']
    final_balance = data['final_balance']
    balance = data['balance']
    total_sent = data['total_sent']
    address = data['address']
    total_received = data['total_received']
    print(address, total_received, balance, final_n_tx, total_sent)
    temp = {
        "address": address,
        "final_n_tx": final_n_tx,
        "n_tx": n_tx,
        "unconfirmed_balance": unconfirmed_balance,
        "final_balance": final_balance,
        "balance": balance,
        "total_sent": total_sent,
        "total_received": total_received,
    }
    addresses.append(temp)

print(len(addresses))

with open('output/cypher_stats.json', 'w') as jsonfile:
    json.dump(addresses, jsonfile, encoding='utf8')