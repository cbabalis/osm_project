""" Module to execute minimum path algorithms and operations such as 
graphs, adjacency lists, etc.
"""

import math
import pandas as pd
import pdb


def compute_distance_between_points(x1, y1, x2, y2):
    """ Method to compute distance between A(x1, y1) and B(x2, y2) and
    to return the result.
    """
    distance = math.sqrt( ((x1 - x2)**2) + ((y1-y2)**2) )
    return distance


def get_node_coords_by_id(node_list, id, col_id='node'):
    """ Method to return the (X, Y) of a node given the id only.
    """
    a_node = node_list[node_list[col_id]==id]
    coords = get_geometry_of_point(a_node.x, a_node.y)
    return coords


def get_geometry_of_point(point):
    """ Method to return the geometry (X, Y) of a point.
    """
    x = float(point.x)
    y = float(point.y)
    return (x, y)


def create_dijkstra_edge_list(edges, nodes):
    """ Method to create a list of edges ready for dijkstra.
    
    Edges should be a list of:
    [(start_node1, end_node1, cost),
     (start_node2, end_node2, cost),
     ...]
    return list_of_edges
    """
    dijkstra_edge_list = []
    for edge in edges.itertuples():
        start_node = edge.u
        end_node = edge.v
        cost = edge.length#compute_travel_cost(start_node, end_node, nodes)
        dijkstra_edge = (start_node, end_node, cost)
        dijkstra_edge_list.append(dijkstra_edge)
    return dijkstra_edge_list


def compute_travel_cost(u, v, node_list, id='osmid'):
    """ Method to compute travel cost based on distance."""
    # check if u, v are in node list
    if u not in node_list[id] or v not in node_list[id]:
        return -1 # TODO should throw an exception here.
    # if they are then get their coordinates and
    u_x, u_y = get_node_coords_by_id(node_list, u, col_id=id)
    v_x, v_y = get_node_coords_by_id(node_list, v, col_id=id)
    # compute their distance
    dist = compute_distance_between_points(u_x, u_y, v_x, v_y)
    # return the distance as the travel cost
    return dist


def refine_dijkstra_results(dijkstra_struct):
    """ Method to refine dijkstra structure that contains results.
    
    Dijkstra structure is as follows:
    (dist, (n1, (n2, (n3, ...))))
    It is a tuple inside a tuple recursively.
    
    Return: distance and a list of nodes defining the path.
    """
    # split distance and path of nodes
    dist = dijkstra_struct[0]
    path = dijkstra_struct[1]
    # process nodes. Iterate tuple until empty and remove nodes one by
    # one until the empty tuple is being found.
    nodes_path = []
    get_nodes_from_tuple(nodes_path, path)
    return dist, nodes_path


def get_nodes_from_tuple(nodes_path, tuple_struct):
    if not tuple_struct:
        return
    nodes_path.append(tuple_struct[0])
    get_nodes_from_tuple(nodes_path, tuple_struct[1])


def get_dijkstra_nodes(nodes, dijkstra_nodes_list, id='osmid'):
    """ Method to find and get nodes that are inside minimum path.
    :param nodes: pandas dataframe for nodes.
    :param dijkstra_nodes_list: a list with dijkstra nodes.
    """
    # create an empty pandas dataframe
    dijkstra_df = pd.DataFrame(columns=nodes.columns)
    # populate new dataframe with the dijkstra nodes
    for dn in dijkstra_nodes_list:
        node = nodes[nodes[id] == dn]
        dijkstra_df = dijkstra_df.append(node)
    return dijkstra_df