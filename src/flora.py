""" Module to fast prototype the merge of the network modeled by networkx tools from OSM and custom input.
"""

import pandas as pd
import osmnx as ox
import input_output_operations as io_ops
import network_operations as net_ops
import network_scenarios as net_scens
import pdb


def assign_POIs_to_graph(graph, pois_df):
    """Method to get a dataframe with points of interest and to
    match the nearest node in the network to each one of them.

    Args:
        graph (graph): graph of the network
        pois_fp (DataFrame): DataFrame that contains points of interest
    """
    # create a list with all nodes to be merged to network
    pois_coords = _get_pois_coords_list(pois_df)
    # finally get a list with all node ids of interest, interpreted to network
    poi_nodes = []
    for poi in pois_coords:
        poi_nodes.append(ox.get_nearest_node(graph, poi))
    return poi_nodes


def _get_pois_coords_list(df, col='coords'):
    """Method to retrieve points of interest from a dataframe,
    to convert them to tuple containing (lat, lon) pairs and
    to return a list full of tuples

    Args:
        df ([type]): [description]
        col (str, optional): [description]. Defaults to 'coords'.

    Returns:
        [type]: [description]
    """
    # create an empty list
    coords_list = []
    raw_coords_list = []
    # get the coordinates as string from the dataframe
    for index, row in df.iterrows():
        raw_coords_list.append(row[col])
    # convert string to comma separated float coordinates
    for elem in raw_coords_list:
        temp = elem.split(",")
        tuplex = (float(temp[0]), float(temp[1]))
        coords_list.append(tuplex)
    return coords_list


def flora(src_graph_fp, csv_src_fp, results_csv_fpath, new_col='traffic'):
    # get the graph from disk
    graph = net_ops.load_graph_from_disk(src_graph_fp)
    nodes, edges = net_ops.get_nodes_edges(graph)
    # read the points of interest to df
    pois_df = io_ops.convert_csv_to_nodes(csv_src_fp)
    assign_POIs_to_graph(graph, pois_df)
    pdb.set_trace()


def main():
    # read input (file with custom data and network)
    # match custom input to network
    # add traffic to edges that connect nodes of custom input
    pass


if __name__ == '__main__':
    main()