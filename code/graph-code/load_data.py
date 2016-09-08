import graphlab as gl
import datetime


def extract_from_csv(data_name):

    ####################################################################################################################

    # list of transactions (hash, coinbase/non-coinbase)

    transactions = gl.SFrame.read_csv("../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/transactions.csv",
                                      header=False,
                                      delimiter=',',
                                      )

    transactions.rename({'X1': 'tx_hash', 'X2': 'coinbase'})

    ####################################################################################################################

    # relationship between transactions and transaction outputs (tx_hash, output key)

    rel_tx_output = gl.SFrame.read_csv("../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/rel_tx_output.csv",
                                       header=False,
                                       delimiter=',',
                                       )

    rel_tx_output.rename({'X1': 'tx_hash', 'X2': 'output_key'})

    ####################################################################################################################

    #  list of blocks (hash, height, timestamp)

    blocks = gl.SFrame.read_csv("../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/blocks.csv",
                                header=False,
                                delimiter=',',
                                )

    blocks.rename({'X1': 'block_hash', 'X2': 'height', 'X3': 'timestamp'})

    ####################################################################################################################

    #  list of transaction outputs (output key, id, value, script type)

    outputs = gl.SFrame.read_csv("../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/outputs.csv",
                                 header=False,
                                 delimiter=',',
                                 )

    outputs.rename({'X1': 'output_key', 'X2': 'id', 'X3': 'value', 'X4': 'script_type'})

    ####################################################################################################################

    #  relationship between blocks and transactions (block_hash, tx_hash)

    rel_block_tx = gl.SFrame.read_csv("../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/rel_block_tx.csv",
                                      header=False,
                                      delimiter=',',
                                      )

    rel_block_tx.rename({'X1': 'block_hash', 'X2': 'tx_hash'})

    ####################################################################################################################

    #  relationship between transactions and transaction outputs (tx_hash, output key)

    rel_input = gl.SFrame.read_csv("../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/rel_input.csv",
                                   header=False,
                                   delimiter=',',
                                   )

    rel_input.rename({'X1': 'tx_hash', 'X2': 'input_key'})

    ####################################################################################################################

    #  input addresses

    input_addresses = gl.SFrame.read_csv("../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/input_addresses.csv",
                                   header=False,
                                   delimiter=',',
                                   )

    input_addresses.rename({'X1': 'tx_hash', 'X2': 'input_address'})

    ####################################################################################################################

    #  relationship between outputs and addresses (output key, address)

    rel_output_address = gl.SFrame.read_csv(
        "../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/rel_output_address.csv",
        header=False,
        delimiter=',',
    )

    rel_output_address.rename({'X1': 'output_key', 'X2': 'address'})

    ####################################################################################################################

    #  list of entity identifiers (entity_id)

    entities = gl.SFrame.read_csv(
        "../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/entities.csv",
        header=False,
        delimiter=',',
    )

    entities.rename({'X1': 'entity_id'})

    ####################################################################################################################

    #  assignment of addresses to entities (address, entity_id)

    rel_address_entity = gl.SFrame.read_csv(
        "../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/rel_address_entity.csv",
        header=False,
        delimiter=',',
    )

    rel_address_entity.rename({'X1': 'address', 'X2': 'entity_id'})

    ####################################################################################################################

    # #  list of identities (address, tag)
    #
    # identities = gl.SFrame.read_csv(
    #     "../../pre-processing/bitgraph/bitcoingraph/" + data_name + "/identities.csv",
    #     header=True,
    #     delimiter=',',
    # )
    #
    # identities.rename({'address': 'output_address'})

    ####################################################################################################################

    return (
    transactions, rel_tx_output, blocks, outputs, rel_block_tx, rel_input, rel_output_address, rel_address_entity,
    entities, input_addresses)

def join(transactions, rel_tx_output, blocks, outputs, rel_block_tx, rel_input, rel_output_address, \
         rel_address_entity, entities, input_addresses):
    data = transactions.join(rel_block_tx, on='tx_hash', how='inner')
    data = data.join(blocks, on='block_hash', how='inner')

    output = rel_tx_output.join(outputs, on='output_key', how='inner')
    output = output.join(rel_output_address, on='output_key', how='inner')
    output.rename({'address': 'output_address'})

    data = data.join(output, on='tx_hash', how='left')
    data = data.join(input_addresses, on='tx_hash', how='left')
    data['timestamp'] = data['timestamp'].astype(datetime.datetime)
    data.add_columns(data['timestamp'].split_datetime(column_name_prefix=None, limit=['year', 'month', 'day']))

    ########################################################################################################################

    download = 'https://static.turi.com/datasets/bitcoin/market-price.csv'

    prices = gl.SFrame.read_csv(download, delimiter=',', header=False, column_type_hints=[str, float])
    prices.rename({'X1': 'timestamp', 'X2': 'close-price'})
    prices['timestamp'] = prices['timestamp'].str_to_datetime('%d/%m/%Y')
    prices.add_columns(prices['timestamp'].split_datetime(column_name_prefix=None, limit=['year', 'month', 'day']))

    ########################################################################################################################

    data = data.join(prices, on=['year', 'month', 'day'], how='left')
    data.remove_column('timestamp.1')
    data.remove_column('output_key')
    # data['dollar'] = data.apply(lambda x: x['value'] * x['close-price'])
    # data['dollar_label'] = data['dollar'].apply(lambda x: '$' + str(round(x, 2)))


    # data = data.join(identities, on='output_address', how='left')

    return data
