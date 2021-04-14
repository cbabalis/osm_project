""" Module to manipulate input/output operations. csv files, data files, etc.

@author: Babis Babalis
@e-mail: babisbabalis@gmail.com
"""

import csv
import pandas as pd
import pdb


def get_u_v_pairs_from_file(in_file):
    """Method to read a csv file and to get all the (u,v) pairs inside
    it with their cost values, too.

    Args:
        in_file (str): file path from disk
    
    Return:
        pairs_list (list): a list of <start_node, end_node, traffic_load> tuples
    
    Example:
    list_of_pairs = get_u_v_pairs_from_file('bob/my_file.csv')
    """
    lines = []
    # read the lines
    with open(in_file, 'r') as a_file:
        lines = a_file.readlines()
    # process the lines of the file accordingly
    nodes_dict = _convert_lines_to_dict(lines)
    pairs_list = _convert_dict_to_every_pair_combo(nodes_dict)
    return pairs_list


def _convert_lines_to_dict(raw_lines):
    a_dict = {}
    for line in raw_lines:
        key, val = line.split(":")
        val = _get_polished_value(val)
        a_dict[key] = val
    return a_dict


def _get_polished_value(raw_val):
    val = raw_val.strip("\n")
    val = val.split(",")
    return val


def _convert_dict_to_every_pair_combo(nodes_dict):
    """method to convert a dictionary of the following form:
    {key1: [],
     key2: [],
     key3: []}
     to a list of all combinations of keys

    Args:
        nodes_dict (dict): dictionary with nodes and values.
    """
    pairs = []
    # get the keys of the dictionary
    nodes = nodes_dict.keys()
    # and iterate it in order to create the adjacency matrix
    for node in nodes:
        pair_set = _create_pairs_starting_with(node, nodes_dict)
        pairs.extend(pair_set)
    return pairs


def _create_pairs_starting_with(key, node_dict):
    pairs = []
    start_node = key
    values = node_dict[key]
    end_nodes = node_dict.keys()
    for val, end_node in zip(values, end_nodes):
        pair = (int(start_node), int(end_node), float(val))
        pairs.append(pair)
    return pairs


def convert_csv_to_nodes(csv_filepath, src_graph_filepath, cols=['latitude', 'longitude', '@id', 'brand']):
    """Method to convert a csv file (from OSM) to nodes that are able to be
    integrated to nodes of a road network.

    Args:
        csv_filepath (str): The path in the disk where the csv file is found.
        src_graph_filepath (str): The path where the network graph is found.
    
    return:
        nodes_list (list): A list of nodes with information to be integrated in a road network.
    """
    # read the raw file from disk
    osm_raw_data_nodes = pd.read_csv(csv_filepath, delimiter='\t')
    # get only the columns needed and rename them (if necessary) to a new dataframe
    osm_nodes_with_coords = osm_raw_data_nodes[['latitude', 'longitude', '@id', 'brand']]
    if '@id' in osm_nodes_with_coords.columns:
        osm_nodes_with_coords.rename(columns={'@id':'node_id'}, inplace=True)
    # return the new dataframe
    pdb.set_trace()
    return osm_nodes_with_coords


def _process_raw_osm_id(df, id_col='node_id'):
    """Method to process the raw osm id and to return just a numeric id.

    Args:
        df (dataframe): pandas dataframe that contains all the nodes of interest.
        id_col (str, optional): name of the column where ID is found. Default is 'node_id'
    
    returns:
        df (dataframe): the updated dataframe
    """
    pass