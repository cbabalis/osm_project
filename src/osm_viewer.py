import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import plotly.express as px
import geopandas as gpd
import shapely.geometry
from shapely.geometry import shape
from shapely import wkt
import numpy as np
import wget
import pdb


def read_data_from_file(fpath, delim='\t'):
    data_df = pd.read_csv(fpath, delimiter=delim)
    return data_df


def create_map_view(df):
    fig = go.Figure(go.Scattermapbox(
        mode = 'markers', #"markers+lines",
        lon = df['longitude'].tolist(), #[23.7412804,23.7483916,23.7551121],
        lat = df['latitude'].tolist(), #[38.0331949,38.0347879,38.0380574],
        marker = {'size': 20}))

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
    print(len(edges))
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
    pdb.set_trace()

    fig = px.line_geo(lat=lats, lon=lons) #, hover_name=names)
    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
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
                cmax=1000),
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
    fpath = '/home/blaxeep/workspace/osm_project/data/all_edges.csv'
    df = read_data_from_file(fpath, delim=',')
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
    view_edges_network(gdf[gdf['traffic']>0])


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
    pdb.set_trace()
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
                               zoom=5)
    fig.show()


def main():
    show_stats_in_map('/home/blaxeep/workspace/osm_project/data/regional_units_dataset_osm/13_regional_units.geojson', stat_to_show='population')
    #first_method()
    #second_method()


if __name__ == '__main__':
    main()