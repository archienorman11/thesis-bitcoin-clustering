import os
import graphlab as gl
import graphlab.aggregate as agg
from graphlab import degree_counting
from graphlab import connected_components
from graphlab import shortest_path
from graphlab import triangle_counting
from graphlab import label_propagation
from graphlab import kcore
from graphlab import graph_coloring
import random
from graphlab import pagerank
from load_data import *
from graph_analytics import *
from utils import *
import datetime
from math import sqrt

########################################################################################################################

# addresses.csv: sorted list of Bitcoin addressed
# blocks.csv: list of blocks (hash, height, timestamp)
# transactions.csv: list of transactions (hash, coinbase/non-coinbase)
# outputs.csv: list of transaction outputs (output key, id, value, script type)
# rel_block_tx.csv: relationship between blocks and transactions (block_hash, tx_hash)
# rel_input.csv: relationship between transactions and transaction outputs (tx_hash, output key)
# rel_output_address.csv: relationship between outputs and addresses (output key, address)
# rel_tx_output.csv: relationship between transactions and transaction outputs (tx_hash, output key)
# entities.csv: list of entity identifiers (entity_id)
# rel_address_entity.csv: assignment of addresses to entities (address, entity_id)

########################################################################################################################

data_name = 'blocks_417500_424572'

if os.path.exists('data/' + data_name + '/'):

    data = gl.SFrame('data/' + data_name)

else:

    transactions, rel_tx_output, blocks, outputs, rel_block_tx, rel_input, rel_output_address, \
    rel_address_entity, entities, input_addresses = extract_from_csv(data_name)

    data = join(transactions, rel_tx_output, blocks, outputs, rel_block_tx, rel_input, rel_output_address,
                rel_address_entity, entities, input_addresses)

    data.save('data/' + data_name + '/')

########################################################################################################################

if os.path.exists('analytics/' + data_name + '/pr_out.csv'):

    print("[INFO] - stats already calculated")

else:

    print("[INFO] - about to calculate stats")

    print(data)

    run_graph_analytics(data, data_name)

pagerank = gl.SFrame.read_csv('analytics/' + data_name + '/pr_out.csv')
pagerank.rename({'__id': 'output_address'})
in_degree = gl.SFrame.read_csv('analytics/' + data_name + '/in_degree.csv')
in_degree.rename({'__id': 'output_address'})
out_degree = gl.SFrame.read_csv('analytics/' + data_name + '/out_degree.csv')
out_degree.rename({'__id': 'output_address'})

########################################################################################################################

data = add_graph_analytics_to_data(data, pagerank, in_degree, out_degree)

########################################################################################################################

data.export_csv('output/' + data_name + '.csv', delimiter=',')

print(data.topk('out_degree', k=10))


# K = int(sqrt(data.num_rows() / 2.0))
#
# kmeans_model = gl.kmeans.create(data, num_clusters=K)
# kmeans_model.show()
