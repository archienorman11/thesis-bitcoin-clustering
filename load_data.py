#LOAD TAGGED DATA

import yaml 
import json
import pandas as pd

def load_data(const_file_name: str):
    with open(const_file_name) as f:
        consts = yaml.safe_load(f)
    
    whoiswho = consts['path_to_whoiswho']
    blockinfo = consts['path_to_blockinfo']
    explorer = consts['path_to_explorer']

    if os.path.exists('../code/identity_scraper/output/'):
        with open(whoiswho) as json_data:
            who = json.load(json_data)
        with open(blockinfo) as json_data:
            block = json.load(json_data) 
        with open(explorer) as json_data:
            explorer = json.load(json_data) 
    else:
        print(consts['cant_find_data'])



    total = who + block + explorer
    print(len(total))