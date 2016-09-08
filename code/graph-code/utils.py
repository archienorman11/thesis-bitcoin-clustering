
def print_head(transactions, rel_tx_output, blocks, outputs, rel_block_tx, rel_input, rel_output_address, rel_address_entity, entities):
    print(transactions.head(n=5))
    print(rel_tx_output.head(n=5))
    print(blocks.head(n=5))
    print(outputs.head(n=5))
    print(rel_block_tx.head(n=5))
    print(rel_input.head(n=5))
    print(rel_output_address.head(n=5))
    print(entities.head(n=5))
    print(rel_address_entity.head(n=5))