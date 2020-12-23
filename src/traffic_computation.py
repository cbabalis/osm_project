""" Module to compute traffic in a network"""

# https://github.com/tallesfelix/directions-with-osm-networkx/blob/master/Creating%20routes%20with%20networkx%20and%20ipyleaflet.ipynb
import networkx as nx
import osmnx as ox
import geopandas as gpd
import pandas as pd
import numpy as np

from ipyleaflet import *
from shapely.geometry import LineString, mapping

import pdb


def create_graph_from_osm_place(place_name, simplify=False, cf=''):
    place_name = "Greece"
    #ox.config(use_cache=True, log_console=True)
    if not cf:
        cf = '["highway"~"motorway|motorway_link|trunk|secondary|primary"]'
    graph = ox.graph_from_place(place_name,
                network_type='drive', simplify, custom_filter=cf)
    #fig, ax = ox.plot_graph(graph)
    return graph


def add_load_column(nodes, name='traffic'):
    nodes[name] = 0


def get_shortest_path(u, v):
    shortest_path = nx.dijkstra_path(graph, u, v, weight='length')
    return shortest_path


def update_nodes(shortest_path, nodes, col_name, cost):
    for n in shortest_path:
        nodes.loc[nodes.osmid == n, col_name] += cost


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
    for pair in all_pairs_list:
        u, v = pair
        edges_list.loc[(edges_list.u == u) & (edges_list.v == v), col_name] += cost


def split_rows(df, li, ids):
    ids_list = ids
    for id in ids_list:
        copied_df = df.copy()
        copied_df.osmid = id
        li.append(copied_df)


def split_osmid_field(loaded_edges):
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


def populate_network_traffic(edges, start1, end1, start2, end2):
    # create edges traffic column and populate it with content
    add_load_column(edges)
    
    # run shortest path (nodes form)
    shortest_path = get_shortest_path(start1, end1)    
    min_path_pairs = get_nodes_pairs(shortest_path)
    update_edge_list(min_path_pairs, edges, 'traffic', 300)
    
    # run shortest path again and add the results
    shortest_path = get_shortest_path(start2, end2)    
    min_path_pairs = get_nodes_pairs(shortest_path)
    update_edge_list(min_path_pairs, edges, 'traffic', 500)
    
    loaded_edges_1 = edges.loc[edges['traffic'] >0]
    return loaded_edges


