""" Module to run network scenarios using network_operations."""

import pandas
import networkx
import network_operations as net_ops
import min_path_ops.min_path_operations as min_ops
import time
import min_path_ops.dijkstra as dijkstra
import pdb


def get_sum_of_two_shortest_paths_edges(graph, edges, start1, end1,
                                        start2, end2, new_col='traffic'):
    # add new column to dataframe
    net_ops.add_new_column_to_dataframe(edges, new_col)
    # execute min path and update edges
    update_edges_list_with_min_path_traffic(graph, edges, start1, end1, new_col)
    update_edges_list_with_min_path_traffic(graph, edges, start2, end2, new_col)
    # get all edges with traffic and return them
    updated_edges = edges.loc[edges[new_col] > 0]
    return updated_edges


def update_edges_list_with_min_path_traffic(graph, edges, start1,
                                            end1, new_col):
    try:
        shortest_path = net_ops.get_shortest_path(graph, start1, end1)
        min_path_pairs = net_ops.get_nodes_pairs(shortest_path)
        net_ops.update_edge_list(min_path_pairs, edges, new_col, 100)
    except networkx.exception.NetworkXNoPath:
        print("no path between ", start1, end1)


def split_list_ids_to_single_rows(edges):
    single_id_rows = net_ops.split_osmid_field(edges)
    single_id_rows_to_df = pandas.concat(single_id_rows)
    return single_id_rows_to_df


def write_traffic_edges_to_csv(edges, results_csv_fpath):
    traffic_edges = edges[edges['traffic']>99]
    single_id_rows_to_df = split_list_ids_to_single_rows(traffic_edges)
    single_id_rows_to_df.to_csv(results_csv_fpath)
    


def scenario_two_paths(graph, edges, s1, e1, s2, e2, new_col,
                       csv_fname):
    traffic_edges = get_sum_of_two_shortest_paths_edges(graph,
                                                        edges,
                                                        s1, e1,
                                                        s2, e2,
                                                        new_col)
    single_id_rows_to_df = split_list_ids_to_single_rows(traffic_edges)
    single_id_rows_to_df.to_csv(csv_fname)


def simple_scenario_ipynb():
    place_name = 'Greece'
    cf = '["highway"~"motorway|motorway_link|trunk|secondary|primary"]'
    net_type = 'drive'
    graph = net_ops.get_network_graph(place_name, net_type, cf)
    nodes, edges = net_ops.get_nodes_edges(graph)
    scenario_two_paths(graph, edges, 3744263637, 300972555, 295512257, 1604968703, 'traffic', 'loaded_edges.csv')


def scenario_all_nodes_with_all(pairs_list, graph, edges, new_col,
                                results_csv_fpath):
    # create and initialize new column
    net_ops.add_new_column_to_dataframe(edges, new_col)
    # get every pair of list of pairs and run a min path between them
    # updating the traffic in each route.
    start_time = time.time()
    pair_counter = 0 # TODO to be removed when not debugging
    #length = len(pairs_list)
    for pair in pairs_list:
        u, v = pair
        update_edges_list_with_min_path_traffic(graph, edges, u, v, new_col)
        #print("pair ", u, v, "\tupdated successfully\t(", pair_counter, "/", length, ")")
        #pair_counter += 1
    print("--- %s seconds min path ---" % (time.time() - start_time))
    # split the list type of id to an id/row and write the result to a file.
    #single_id_rows_to_df = split_list_ids_to_single_rows(edges)
    #single_id_rows_to_df.to_csv(results_csv_fpath)
    #return single_id_rows_to_df


def scenario_all_in_all(src_graph_fp, csv_src_fp, results_csv_fpath, node):
    # read the csv file and get the list of nodes
    df = pandas.read_csv(csv_src_fp, sep=';')
    nodes_list = df[node].to_list()
    combo_list = net_ops.get_all_list_combinations(nodes_list)
    
    # get the network graph
    #cf = '["highway"~"motorway|motorway_link|trunk|secondary|primary"]'
    #graph = net_ops.get_network_graph('Greece', 'drive', cf)
    graph = net_ops.load_graph_from_disk(src_graph_fp)
    nodes, edges = net_ops.get_nodes_edges(graph)
    scenario_all_nodes_with_all(combo_list, graph, edges, 'traffic', results_csv_fpath)
    write_traffic_edges_to_csv(edges, results_csv_fpath)


def custom_dijkstra(src_graph_fp, results_csv_fpath, node):
    graph = net_ops.load_graph_from_disk(src_graph_fp)
    nodes, edges = net_ops.get_nodes_edges(graph)
    dijkstra_edges = min_ops.create_dijkstra_edge_list(edges, nodes)
    dijkstra_path = dijkstra.dijkstra(dijkstra_edges, 295512257, 1604968703)
    
    dist, dijkstra_node_list = min_ops.refine_dijkstra_results(dijkstra_path)
    dijkstra_nodes_df = min_ops.get_dijkstra_matching_df(nodes, dijkstra_node_list, id='osmid')
    # write dijkstra nodes to csv
    dijkstra_nodes_df.to_csv('../results/dijkstra_nodes.csv')
    # write dijkstra edges to csv
    dijkstra_edges_df = min_ops.get_dijkstra_matching_df(edges, dijkstra_node_list, id='u')
    dijkstra_edges_df.to_csv('../results/dijkstra_edges.csv')


def custom_dijkstra_all_vs_all(src_graph_fp, csv_src_fp, results_csv_fpath, node):
    # read the csv file and get the list of nodes
    df = pandas.read_csv(csv_src_fp, sep=';')
    nodes_list = df[node].to_list()
    combo_list = net_ops.get_all_list_combinations(nodes_list)
    graph = net_ops.load_graph_from_disk(src_graph_fp)
    nodes, edges = net_ops.get_nodes_edges(graph)
    # get edges of network in appropriate form for custom dijkstra
    dijkstra_edges = min_ops.create_dijkstra_edge_list(edges, nodes)
    #TODO here we are
    custom_dijkstra_all_nodes_vs_all(combo_list, graph, edges, 'traffic',
                                dijkstra_edges, results_csv_fpath)


def custom_dijkstra_all_nodes_vs_all(pairs_list, graph, edges, new_col,
                                dijkstra_node_list, results_csv_fpath):
    # create and initialize new column
    net_ops.add_new_column_to_dataframe(edges, new_col)
    # get every pair of list of pairs and run a min path between them
    # updating the traffic in each route.
    start_time = time.time()
    pair_counter = 0 # TODO to be removed when not debugging
    #length = len(pairs_list)
    for pair in pairs_list:
        u, v = pair
        update_edges_list_with_custom_dijkstra_traffic(graph, edges, u, v, new_col, dijkstra_node_list)
        #print("pair ", u, v, "\tupdated successfully\t(", pair_counter, "/", length, ")")
        #pair_counter += 1
    print("--- %s seconds custom min path ---" % (time.time() - start_time))


def update_edges_list_with_custom_dijkstra_traffic(graph, edges, start1,
                                            end1, new_col, dijkstra_edges):
    try:
        dijkstra_path = dijkstra.dijkstra(dijkstra_edges, start1, end1)
        dist, dijkstra_node_list = min_ops.refine_dijkstra_results(dijkstra_path)
        min_path_pairs = net_ops.get_nodes_pairs(dijkstra_node_list)
        net_ops.update_edge_list(min_path_pairs, edges, new_col, 100)
    except TypeError:
        print("no path between ", start1, end1)


def k_best_scenario(src_graph_fp, results_csv_fpath, node, k_nodes=[]):
    """ Method to run a k-best scenario with mandatory "passing"
    through every one of the k_nodes. If no k_nodes list is given then
    a simple dijkstra is executed (k=1).
    
    :param:
    """
    # load network
    graph = net_ops.load_graph_from_disk(src_graph_fp)
    nodes, edges = net_ops.get_nodes_edges(graph)
    dijkstra_edges = min_ops.create_dijkstra_edge_list(edges, nodes)
    # initialize the k_best parameters
    k_res = []
    k_nodes = [3744263637, 300972555, 295512257, 1604968703]
    min_ops.k_best(dijkstra_edges, k_nodes, '', '', k_res)
    dist, k_best_list = min_ops.refine_k_best_results(k_res)
    pdb.set_trace()


def main():
    k_best_scenario('../results/greece.graphml', 'results.csv', 'osmid',)
    #custom_dijkstra_all_vs_all('../results/greece.graphml', '../data/POINTS_NUTS3_MAINLAND3.csv', 'skat', 'node_id')
    #custom_dijkstra('../results/greece.graphml', 'results.csv', 'osmid',)
    #scenario_all_in_all('../results/greece.graphml', '../data/POINTS_NUTS3_MAINLAND3.csv', '../results/POINTS_NUTS3_MAINLAND3_RESULTS.csv', 'node_id')
    #simple_scenario_ipynb()


if __name__ == '__main__':
    main()