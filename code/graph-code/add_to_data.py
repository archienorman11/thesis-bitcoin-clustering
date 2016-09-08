import graphlab as gl

def add_graph_analytics_to_data(data, pagerank, in_degree, out_degree):
    data = data.join(pagerank, on='output_address', how='left')
    data = data.join(in_degree, on='output_address', how='left')
    data = data.join(out_degree, on='output_address', how='left')

    return data