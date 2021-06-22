import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import plotly.express as px
import geopandas as gpd
import shapely.geometry
from shapely.geometry import shape
from shapely import wkt
import numpy as np
import osmnx as ox
import wget
import network_operations as net_ops
import pdb


def read_data_from_file(fpath, delim='\t'):
    data_df = pd.read_csv(fpath, delimiter=delim)
    return data_df


def create_map_view(df):
    fig = go.Figure(go.Scattermapbox(
        mode = 'markers', #"markers+lines",
        lon = df['longitude'].tolist(), #[23.7412804,23.7483916,23.7551121],
        lat = df['latitude'].tolist(), #[38.0331949,38.0347879,38.0380574],
        marker = {'size': 30}))

    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = [-50, -60,40],
        lat = [30, 10, -20],
        marker = {'size': 10}))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 10, 'lat': 10},
            'style': "open-street-map", #"stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1})

    return fig


def map_traffic_to_color(thickness, colors=[]):
    """Method to map traffic to colors.

    Args:
        thickness (list): traffic value for each edge
    """
    # if color list is empty, have just 3 colors.
    if not colors:
        colors = [1000, 2000, 3000]
        color_dict = {1:'green', 2:'yellow', 3:'red'}
    intervals = len(colors)
    min_val, thres = _get_thresholds(thickness, intervals)
    # if instance is not none:
    # if condition is True
    # then replace value with color
    for i in range(1, intervals+1):
        threshold = min_val + i*thres
        thickness = [color_dict[i] if _are_conditions_true(elem, threshold) else elem for elem in thickness]
    return thickness
                
    # for i in range(1, intervals+1):
    #     thickness = [color[i-1] if ele < i else ele for ele in thickness]
    # for elem in color_dict:
    #     thickness = [color_dict[elem] if elem == li_elem else li_elem for li_elem in thickness]
    # return thickness


def _are_conditions_true(elem, val):
    if isinstance(elem, int) or isinstance(elem, float):
        if elem <= val:
            return True
    return False


def _get_thresholds(a_list, intervals_num):
    min_val = _get_min_val(a_list)
    max_val = _get_max_val(a_list)
    threshold_interval = (max_val - min_val) / intervals_num
    return min_val, threshold_interval


def _get_min_val(a_list, default_min=100000, inst=int):
    min_val = default_min
    for elem in a_list:
        if isinstance(elem, inst):
            if elem < min_val:
                min_val = elem
    return min_val


def _get_max_val(a_list, default_max=-1, inst=int):
    max_val = default_max
    for elem in a_list:
        if isinstance(elem, inst):
            if elem > max_val:
                max_val = elem
    return max_val
            


def _is_eligible_to_color_update(val, thres):
    if val:
        if val < thres:
            return True
    return False


def view_edges_network(edges):
    """ Method to show edges (roads) of a network

    Args:
        edges (dataframe): Dataframe from networkx analysis of a graph for edges.
    """
    lats = []
    lons = []
    names = []
    thickness = []
    print("edges are ", len(edges))
    thousands_counter = 0
    for feature, name, traff in zip(edges.geometry, edges.name, edges.traffic):
        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        for linestring in linestrings:
            x, y = linestring.xy
            lats = np.append(lats, y)
            lons = np.append(lons, x)
            names = np.append(names, [name]*len(y))
            thickness = np.append(thickness, [traff]*len(y))
            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            thickness = np.append(thickness, None)
            thousands_counter += 1
        if thousands_counter % 1000 == 0:
            print(thousands_counter)
    
    colors = map_traffic_to_color(thickness)
    colors = np.array(colors)

    fig = px.line_geo(lat=lats, lon=lons) #, hover_name=names)
    fig.add_trace(go.Scattermapbox(
        #mode = "markers+lines",
        mode = "lines",
        lon = [-50, -60,40],
        lat = [30, 10, -20],
        marker = {'size': 10}))
    fig.add_trace(
        go.Scattermapbox(
            lon = lons,
            lat = lats,
            marker=dict(
                size=10,
                showscale=True,
                colorscale=[[0, 'green'],
                            [1, 'red']],
                cmin=0,
                cmax=2000),
            line={'color':'red'},
        )
    )
    fig.add_trace(
        go.Scattermapbox(
            lon = lons,
            lat = lats,
            mode='lines',
            line={'color':'green'},
        )
    )
    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1})
    fig.show()


def first_method():
    fpath = '/home/blaxeep/workspace/osm_project/data/super_sample.csv'
    df = read_data_from_file(fpath, delim=',')
    fig = create_map_view(df)
    fig.show()


def second_method():
    #fpath = '/home/blaxeep/workspace/osm_project/data/all_edges.csv'
    fpath = '/home/blaxeep/Downloads/bab_edges.csv'
    df = read_data_from_file(fpath, delim=',')
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
    view_edges_network(gdf[gdf['traffic']>0])
    #view_edges_network(gdf)


def show_stats_in_map(stats_fpath, stat_to_show=''):
    """Method to show stats in a map.

    Args:
        stats_fpath (str): Path to file.
        stat_to_show (str): Variable to show variance. It usually is a pandas column.
    """
    # load data from disk to geopandas
    gdf = gpd.read_file(stats_fpath)
    # update the geopandas data getting rid of zeros, None values
    gdf[stat_to_show] = gdf[stat_to_show].fillna(0)
    gdf[stat_to_show] = pd.to_numeric(gdf[stat_to_show])
    gdf = gdf[gdf[stat_to_show] > 0]
    # load to map and print
    print_gdf_to_map(gdf, stat_to_show)


def print_gdf_to_map(gdf, stat_to_show):
    """Method to print a geopandas data set to map.

    Args:
        gdf ([type]): [description]
        stat_to_show ([type]): [description]
    """
    fig = px.choropleth_mapbox(gdf,
                               geojson=gdf['geometry'],
                               locations=gdf.index,
                               color=stat_to_show,
                               center={"lat": 30.5517, "lon": 23.7073},
                               mapbox_style="open-street-map",
                               opacity=0.35,
                               zoom=5)
    fig.show()


def od_viewer_to_map(csv_file, graph_file, lonlat_centres_file):
    """Method to view data of an OD-Matrix to a map.

    Args:
        csv_file ([type]): [description]
        graph_file ([type]): [description]
    """
    # load graph and data with loads for cities from csv_file
    df = read_data_from_file(csv_file, ',')
    net_graph = net_ops.load_graph_from_disk(graph_file)
    nodes, edges = net_ops.get_nodes_edges(net_graph)
    # assign cities to graph nodes
    reg_units_df = read_data_from_file(lonlat_centres_file, ',')
    node_id_list = _assign_net_node_to_reg_unit(reg_units_df, net_graph)
    # replace names of regional units with node ids.
    df = _replace_od_columns_with_node_ids(df, reg_units_df)
    # compute min path between cities in the network
    #nodes_pairs_list = create_nodes_pairs(node_id_list)
    nodes_pairs_list = extract_node_pairs_from_od(df)
    # load edges of network with the corresponding loads
    _update_edges_with_loads(net_graph, edges, nodes_pairs_list)
    # return loaded edges
    pdb.set_trace()
    # load loaded edges to map


def _assign_net_node_to_reg_unit(df, net_graph):
    # create a new column to df with node ids
    df['Node ID'] = np.nan
    # get longitude and latitude values to respective lists
    lat_list = df['lat']
    lon_list = df['lon']
    # create lat, lon pairs
    coords_list = []
    for lat, lon in zip(lat_list, lon_list):
        coords = (lat, lon)
        coords_list.append(coords)
    # get the nearest node to the lat, lon pair
    node_id_list = []
    for coords in coords_list:
        lat, lon = coords
        node_id = ox.get_nearest_node(net_graph, (lat,lon), method='haversine') #, return_dist=True)
        node_id_list.append(node_id)
    # assign it to a new list and then add it to the new column
    df['Node ID'] = node_id_list
    return node_id_list


def create_nodes_pairs(node_id_list):
    """Method to create all possible pairs of node ids.
    Given a list of node ids, combine each id with any other and
    return a list of tuples of <u, v> nodes

    Args:
        node_id_list (list): list of string node ids
    
    return:
        list of (u, v) tuples.
    """
    combo_list = []
    iter_list = node_id_list
    # for each element in list:
    for elem in node_id_list:
        # remove element from list and get all possible combinations and
        # append the combinations to a new list
        iter_list.remove(elem)
        for iter_elem in iter_list:
            combo_list.append((elem, iter_elem))
    # return the list
    return combo_list


def extract_node_pairs_from_od(od_df):
    """Method to extract node pairs from an od matrix.
    
    This method gets all possible combinations of an od matrix
    assigning to each pair the cost of the transfer between them.

    Args:
        od_df (Dataframe): Origin-Destination matrix.
    return:
        list of <u, v, cost> pairs.
    """
    node_pairs = []
    # get all node ids.
    od_ids = od_df.columns.tolist()
    del od_ids[0]
    # combine each node id with each other assigning a cost too.
    for col in od_ids:
        costs = od_df[col]
        # create a tuple of the data above and add it to a list.
        for row, cost in zip(od_ids, costs):
            node_pairs.append((row, col, cost))
    return node_pairs


def _replace_od_columns_with_node_ids(od_df, node_ids_df, val_col='Node ID', key_col='Reg_unit'):
    """Method to replace all OD Matrix columns' names with the
    corresponding node ids.

    Args:
        od_df (Dataframe): Dataframe that represents an OD-Matrix. Columns
        have string values of regions
        node_ids_df (Dataframe): Contains information regarding the regional
        units, their location on map and the corresponding node ids to our network.
        
    Return:
        dataframe with node ids instead of string names as columns
    """
    # get all od-matrix columns in a list
    region_names_list = od_df.columns.tolist()
    # create a dictionary of <region: node_id> pairs from the node_ids_df dataframe
    reg_node_dict = pd.Series(node_ids_df[val_col].values, index=node_ids_df[key_col]).to_dict()
    # replace all names of the od-matrix with node ids and return
    region_names_list = [reg_node_dict.get(x, x) for x in region_names_list]
    od_df.columns = region_names_list
    return od_df


def update_edges_list_with_min_path_traffic(graph, edges, start1,
                                            end1, new_col, val=100):
    try:
        shortest_path = net_ops.get_shortest_path(graph, start1, end1)
        min_path_pairs = net_ops.get_nodes_pairs(shortest_path)
        net_ops.update_edge_list(min_path_pairs, edges, new_col, val)
    except networkx.exception.NetworkXNoPath:
        print("no path between ", start1, end1)


def _update_edges_with_loads(graph, edges, nodes_pairs_list):
    import network_scenarios as net_scens
    net_ops.add_new_column_to_dataframe(edges, 'traffic')
    for pair in nodes_pairs_list:
        u, v, cost = pair
        if u is not v:
            net_scens.update_edges_list_with_min_path_traffic(
                graph, edges, u, v, 'traffic', cost
            )


def main():
    #show_stats_in_map('/home/blaxeep/workspace/osm_project/data/regional_units_dataset_osm/13_regional_units.geojson', stat_to_show='population')
    #first_method()
    #second_method() # it has the network road
    root_dir = '/home/blaxeep/workspace/osm_project/data/viewer_data/'
    graph_src = root_dir + 'greece-graph.graphml'
    od_src = root_dir + 'od_matrix.csv'
    reg_src = root_dir + 'reg_units_coords_node_id.csv'
    od_viewer_to_map(od_src, graph_src, reg_src)


if __name__ == '__main__':
    main()