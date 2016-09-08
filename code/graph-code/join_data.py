import graphlab as gl
import datetime


def join(transactions, rel_tx_output, blocks, outputs, rel_block_tx, rel_input, rel_output_address, \
         rel_address_entity, entities, input_addresses, identities):
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
    data['dollar'] = data.apply(lambda x: x['value'] * x['close-price'])
    data['dollar_label'] = data['dollar'].apply(lambda x: '$' + str(round(x, 2)))
    data = data.fillna('input_address', 0)

    data = data.join(identities, on='output_address', how='left')

    return data
