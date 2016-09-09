Archie Norman - Classification of Bitcoin transactions based on supervised machine learning and transaction network metrics.

Abstract: The Bitcoin currency is a publicly available, transparent, large scale network in which every single transaction can be analysed. Multiple tools are used to extract binary information, pre-process data and train machine learning models from the decentralised blockchain. As Bitcoin popularity increases both with consumers and businesses alike, this paper looks at the threat to privacy faced by users through commercial adoption by deriving user attributes, transaction properties and inherent idioms of the network. We define the Bitcoin network protocol, describe heuristics for clustering, mine the web for publicly available user information and finally train supervised learning models. We show that two machine learning algorithms perform  successfully in clustering the Bitcoin transactions based on only graphical metrics measured from the transaction network. The Logistic Regression algorithm achieves an F1 score of 0.731 and the Support Vector Machines achieves an F1 score of 0.727. This work demonstrates the value of machine learning and network analysis for business intelligence; on the other hand it also reveals the potential threats to user privacy. 

## Prerequesites

Please note that installing the bitcoin blockchain and running all scripts may take ~ 10 days as the blockchain download is around 160GB and needs to be indexed. The instructions given here are from the bitcoingraph tool.

### Bitcoin Core setup and configuration

First, install the current version of Bitcoin Core (v.11.1), either from [source](https://github.com/bitcoin/bitcoin) or from a [pre-compiled executable](https://bitcoin.org/en/download).

Once installed, you'll have access to three programs: `bitcoind` (= full peer), `bitcoin-qt` (= peer with GUI), and `bitcoin-cli` (RPC command line interface). The following instructions have been tested with `bitcoind` and assume you can start and run a Bitcoin Core peer as follows:

    bitcoind -printtoconsole

Second, you must make sure that your bitcoin client accepts JSON-RPC connections by modifying the [Bitcoin Core configuration file][bc_conf] as follows:

    # server=1 tells Bitcoin-QT to accept JSON-RPC commands.
    server=1

    # You must set rpcuser and rpcpassword to secure the JSON-RPC api
    rpcuser=your_rpcuser
    rpcpassword=your_rpcpass

    # How many seconds bitcoin will wait for a complete RPC HTTP request.
    # after the HTTP connection is established.
    rpctimeout=30

    # Listen for RPC connections on this TCP port:
    rpcport=8332

Test whether the JSON-RPC interface is working by starting your Bitcoin Core peer (...waiting until it finished startup...) and using the following cURL request (with adapted username and password):

    curl --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }' -H 'content-type: text/plain;' http://your_rpcuser:your_rpcpass@localhost:8332/


Third, since Bitcoingraph needs to access non-wallet blockchain transactions by their ids, you need to enable the transaction index in the Bitcoin Core database. This can be achieved by adding the following property to your `bitcoin.conf`

    txindex=1

... and restarting your Bitcoin core peer as follows (rebuilding the index can take a while):

    bitcoind -reindex


Test non-wallet transaction data access by taking an arbitrary transaction id and issuing the following request using cURL:

    curl --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["110ed92f558a1e3a94976ddea5c32f030670b5c58c3cc4d857ac14d7a1547a90", 1] }' -H 'content-type: text/plain;' http://your_rpcuser:your_rpcpass@localhost:8332/


Finally, bitcoingraph also makes use of Bitcoin Core's HTTP REST interface, which is enabled using the following parameter:

    bitcoind -rest

Test it using some sample block hash

    http://localhost:8332/rest/block/000000000000000e7ad69c72afc00dc4e05fc15ae3061c47d3591d07c09f2928.json


When you reached this point, your Bitcoin Core setup is working. Terminate all running bitcoind instances and launch a new background daemon with enabled REST interface

    bitcoind -daemon -rest


### Bitcoingraph library setup

Bitcoingraph is being developed in Python 3.4. Make sure it is running on your machine:

    python --version


Now clone Bitcoingraph...

    git clone https://github.com/behas/bitcoingraph.git


...test and install the Bitcoingraph library:

    cd bitcoingraph
    pip install -r requirements.txt
    py.test
    python setup.py install


### Mac OSX specifics

Running bitcoingraph on a Mac requires coreutils to be installed

    homebrew install coreutils

### Step 1: Create transaction dump from blockchain

Bitcoingraph provides the `bcgraph-export` tool for exporting transactions in a given block range from the blockchain. The following command exports all transactions contained in block range 0 to 1000 using Neo4Js header format and separate CSV header files:

    bcgraph-export 417500 424572 -u your_rpcuser -p your_rpcpass

The following CSV files are created (with separate header files):

* addresses.csv: sorted list of Bitcoin addressed
* blocks.csv: list of blocks (hash, height, timestamp)
* transactions.csv: list of transactions (hash, coinbase/non-coinbase)
* outputs.csv: list of transaction outputs (output key, id, value, script type)
* rel_block_tx.csv: relationship between blocks and transactions (block_hash, tx_hash)
* rel_input.csv: relationship between transactions and transaction outputs (tx_hash, output key)
* rel_output_address.csv: relationship between outputs and addresses (output key, address)
* rel_tx_output.csv: relationship between transactions and transaction outputs (tx_hash, output key)


### Step 2: Compute entities over transaction dump

The following command computes entities for a given blockchain data dump:

    bcgraph-compute-entities -i blocks_417500_424572

Two additional files are created:

* entities.csv: list of entity identifiers (entity_id)
* rel_address_entity.csv: assignment of addresses to entities (address, entity_id)


## Contributors for the above installation and code

* [Bernhard Haslhofer](mailto:bernhard.haslhofer@ait.ac.at)
* [Roman Karl](mailto:roman.karl@ait.ac.at)

Ensure Python 2.7.x

## Create a new conda environment with Python 2.7.x

    conda create -n gl-env python=2.7 anaconda

## Activate the conda environment

    source activate gl-env

Ensure pip version \>= 7

### Ensure pip is updated to the latest version, miniconda users may need to install pip first, using 'conda install pip'

    conda update pip

### Install GraphLab Create

## Install your licensed copy of GraphLab Create

    pip install --upgrade --no-cache-dir https://get.graphlab.com/ \
    GraphLab-Create/2.1/your registered email address here/your product \
    key here/GraphLab-Create-License.tar.gz

## Ensure installation of IPython and IPython Notebook

## Install or update IPython and IPython Notebook

    conda install ipython-notebook

### Run the prep-processing code

    cd notebooks

    jupyter notebook

# Run

    Calculate users, add graph metrics, add categorical tags.ipynb

    Build supervised learning models.ipynb





