""" This module executes network operations.

Module to create graph from shapefiles or osm data, to run minimum paths
and to read/write from/to csv files geodata.
"""

import networkx as nx
import osmnx as ox
import geopandas as gpd
import pandas as pd
import numpy as np
from ipyleaflet import *
from shapely.geometry import LineString, mapping

# debugger. Comment/uncomment depending on case.
import pdb


def get_network_graph(place_name, net_type, custom_filter):
    """ Method to get OSM data and to convert it to network graph.
    
    place_name -- the name of a place.
    net_type -- network type (for instance 'drive')
    custom_filter -- a custom filter for selecting particular parts of the network.
    
    Returns a graph of the selected network.
    """
    ox.config(use_cache=True, log_console=True)
    graph = ox.graph_from_place(place_name, network_type=net_type,
                                custom_filter=custom_filter)
    return graph


def get_nodes_edges(graph):
    """ Returns nodes and edges of a network graph in a tuple."""
    nodes, edges = ox.graph_to_gdfs(graph)
    return (nodes, edges)


def add_new_column_to_dataframe(df, name='traffic'):
    """ Adds a new column to a df and initializes it with 0."""
    df[name] = 0


def get_shortest_path(g, u, v, weight='length'):
    """ Returns a list of nodes that conclude the shortest path between two nodes of a network.
    
    Parameters:
    g -- graph to perform the shortest path
    u -- start node.
    v -- end node.
    weight -- the "cost" param for going from node a to node b. (default: length)
    
    Returns a list of nodes.
    """
    shortest_path = nx.dijkstra_path(g, u, v, weight=weight)
    #shortest_path = nx.astar_path(g, u, v, weight=weight)
    return shortest_path


def get_nodes_pairs(a_list):
    """ Algorithm:
    - create a stop condition (the last element of the input list)
    - iterate the list keeping the current and the next element.
    - return pairs of (current, next) nodes and append them to a new list.
    - when the next node equals the last item of the list (stop condition), then
    - exit the loop and
    - return the list.
    
    :param: list: a list of ints
    :return: list of tuples (containing <u, v> pairs)
    """
    all_pairs = []
    stop_condition = a_list[-1]
    cont = True
    while cont:
        for idx, elem in enumerate(a_list):
            u = elem
            v = a_list[(idx+1) % len(a_list)]
            if v == stop_condition:
                cont = False
            else:
                all_pairs.append((u, v))
    return all_pairs

def update_edge_list(all_pairs_list, edges_list, col_name, cost):
    """ Method to add a value (cost) to each edge in edges_list."""
    for pair in all_pairs_list:
        u, v = pair
        edges_list.loc[(edges_list.u == u) & (edges_list.v == v), col_name] += cost


def split_rows(df, li, ids):
    """ Method to get a list of values and to assign each value to one row."""
    ids_list = ids
    for id in ids_list:
        copied_df = df.copy()
        copied_df.osmid = id
        li.append(copied_df)


def split_osmid_field(loaded_edges):
    """ Method to split osmid field in a dataframe of edges."""
    splitted_rows = []
    print(len(splitted_rows))
    for i in range(len(loaded_edges)):
        df = loaded_edges.iloc[[i]]
        osmid_contents = (df.osmid.to_list()).pop()
        #pdb.set_trace()
        if type(osmid_contents) is not list:
            splitted_rows.append(df)
        else:
            split_rows(df, splitted_rows, osmid_contents)
    return splitted_rows


def get_all_list_combinations(a_list):
    """ Method to get all list combinations by two.
    Returns a new list of tuples with every possible combination.
    """
    combos_list = []
    for u in range(len(a_list)-1):
        for v in range(u+1, len(a_list)):
            combos_list.append((a_list[u], a_list[v]))
    return combos_list


def load_graph_from_disk(src_filepath):
    """ Method to load and return a graph (in graphml) to memory.
    """
    graph = ox.load_graphml(src_filepath)
    return graph