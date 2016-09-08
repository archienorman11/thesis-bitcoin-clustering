#!/usr/bin/env python

import csv
import collections
import json

cnt = collections.Counter()

sort = open('output/sort.csv')
gambling_sample = open('output/gambling.csv')
finance_sample = open('output/finance.csv')
services_sample = open('output/services.csv')
charity_sample = open('output/charity.csv')
junk_sample = open('output/junk.csv')

sort = csv.reader(sort)
gambling_sample = csv.reader(gambling_sample)
finance_sample = csv.reader(finance_sample)
services_sample = csv.reader(services_sample)
charity_sample = csv.reader(charity_sample)
junk_sample = csv.reader(junk_sample)

sort = list(sort)

gamble = []
for j in gambling_sample:
    for val in j:
        gamble.append(val)

finance = []
for j in finance_sample:
    for val in j:
        finance.append(val)

services = []
for j in services_sample:
    for val in j:
        services.append(val)

charity = []
for j in charity_sample:
    for val in j:
        charity.append(val)

junk = []
for j in junk_sample:
    for val in j:
        junk.append(val)

def update_all(name, id):
        for b in dict_list:
            if b['source'] == name:
                b['tag'] = id

def update_from_lists():
    for j in dict_list:
        for k in gamble:
            if str(k) in str(j['source']):
                update_all(j['source'], 1)
        for f in services:
            if str(f) in str(j['source']):
                update_all(j['source'], 4)
        for l in finance:
            if str(l) in str(j['source']):
                update_all(j['source'], 3)
        for t in charity:
            if str(t) in str(j['source']):
                update_all(j['source'], 2)
        for v in junk:
            if str(v) in str(j['source']):
                update_all(j['source'], 5)


def categorise_to_list():
    for item in dict_list:
        if item['tag'] == 0:
            answer = int(input("%s - (1=Gambling, 2=Charity, 3=Finance, 4=Services, 5=Scam/Junk): " % item['source']))
            if answer == 1:
                with open('gambling.csv','a') as g:
                    g.write(item['source'] + "\n")
                    update_all(item['source'], 1)
            elif answer == 2:
                with open('charity.csv','a') as c:
                    c.write(item['source'] + "\n")
                    update_all(item['source'], 2)
            elif answer == 3:
                with open('finance.csv','a') as f:
                    f.write(item['source'] + "\n")
                    update_all(item['source'], 3)
            elif answer == 4:
                with open('services.csv','a') as s:
                    s.write(item['source'] + "\n")
                    update_all(item['source'], 4)
            elif answer == 5:
                with open('junk.csv','a') as j:
                    j.write(item['source'] + "\n")
                    update_all(item['source'], 5)
            elif answer == 10:
                get_stats()
            elif answer == 100:
                create_json_output()
                break
            elif answer == 1000:
                break

        else:
            print('done')

def get_stats():
    un_tagged = 0
    tagged = 0
    for p in dict_list:
        if p['tag'] == 0:
            un_tagged += 1
            cnt[p['source']] += 1
        else:
            tagged += 1

    print(cnt.most_common(30))
    print(tagged)
    print(un_tagged)

def create_json_output():
    temp_list = []
    for i in dict_list:
        temp = {i['address']: i['tag']}
        temp_list.append(temp)
    with open('output/output.json', 'w') as jsonfile:
        json.dump(temp_list, jsonfile)

dict_list = []
for i in sort:
    dict = {"address": i[0], "source": i[1], "tag": 0}
    dict_list.append(dict)

update_from_lists()
categorise_to_list()



