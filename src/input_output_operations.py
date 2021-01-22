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
        pair = (start_node, end_node, val)
        pairs.append(pair)
    return pairs
            


def main():
    u_v = get_u_v_pairs_from_file('../data/tat_4_step_csv.csv')
    pdb.set_trace()


if __name__ == '__main__':
    main()