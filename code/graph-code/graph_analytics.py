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

def run_graph_analytics(data, data_name):

    ####################################################################################################################

    g = gl.SGraph().add_edges(data, src_field='input_address', dst_field='output_address')

    print(g)

    ####################################################################################################################

    transaction_count = data.groupby(['year', 'month'], agg.COUNT).sort(['year', 'month'], ascending=True)
    n_month = transaction_count.num_rows()
    transaction_count['label'] = transaction_count['month'].astype(str) + "/" + transaction_count['year'].astype(str)
    print(transaction_count)

    ####################################################################################################################

    deg = degree_counting.create(g)
    deg_graph = deg['graph'] # a new SGraph with degree data attached to each vertex

    in_degree = deg_graph.vertices[['__id', 'in_degree']]
    out_degree = deg_graph.vertices[['__id', 'out_degree']]



    in_degree.export_csv('analytics/' + data_name + '/in_degree.csv', delimiter=',')
    out_degree.export_csv('analytics/' + data_name + '/out_degree.csv', delimiter=',')

    pr = gl.pagerank.create(g)
    pr_out = pr['pagerank']
    pr_out.export_csv('analytics/' + data_name + '/pr_out.csv', delimiter=',')

def add_graph_analytics_to_data(data, pagerank, in_degree, out_degree):
    data = data.join(pagerank, on='output_address', how='left')
    data = data.join(in_degree, on='output_address', how='left')
    data = data.join(out_degree, on='output_address', how='left')

    return data


    ####################################################################################################################

    # def increment_degree(src, edge, dst):
    #     src['degree'] += 1
    #     dst['degree'] += 1
    #     return (src, edge, dst)
    #
    # g.vertices['degree'] = 0
    # g = g.triple_apply(increment_degree, mutated_fields=['degree'])
    # print(g.vertices.sort('degree', ascending=False))
    #
    #
    # ####################################################################################################################
    #
    # cc = connected_components.create(g)
    # print(cc.summary())
    # print(cc.list_fields())
    #
    # cc_ids = cc['component_id']      # equivalent to the above line
    # cc_graph = cc['graph']
    # print(cc_graph)
    #
    # ####################################################################################################################
    #
    # # sp = shortest_path.create(g, source_vid=0)
    # # sp_sframe = sp['distance']
    # # sp_graph = sp['graph']
    # # path = sp.get_path('98')
    # # print(sp_graph)
    #
    # ####################################################################################################################
    #
    # tc = triangle_counting.create(g)
    # tc_out = tc['triangle_count']
    # print(tc_out)
    #
    # ####################################################################################################################
    #
    # # def init_label(vid):
    # #     x = random.random()
    # #     if x > 0.9:
    # #         return 0
    # #     elif x < 0.1:
    # #         return 1
    # #     else:
    # #         return None
    # # g.vertices['labels'] = g.vertices['__id'].apply(init_label, int)
    # # m = label_propagation.create(g)
    # # labels = m['labels']
    #
    # ####################################################################################################################
    #
    # color = graph_coloring.create(g)
    # color_id = color['color_id']
    # num_colors = color['num_colors']
    # print(color_id)
    #
    # ####################################################################################################################
    #
    # kc = kcore.create(g)
    # kcore_id = kc['core_id']
    # print(kcore)

    ####################################################################################################################
