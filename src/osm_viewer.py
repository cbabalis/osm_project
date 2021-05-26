import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import geopandas as gpd
import shapely.geometry
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
        marker = {'size': 10}))

    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = [-50, -60,40],
        lat = [30, 10, -20],
        marker = {'size': 10}))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1})

    return fig


def view_edges_network(edges):
    """ Method to show edges (roads) of a network

    Args:
        edges (dataframe): Dataframe from networkx analysis of a graph for edges.
    """
    lats = []
    lons = []
    names = []
    print(len(edges))
    thousands_counter = 0
    for feature, name in zip(edges.geometry, edges.name):
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
            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            thousands_counter += 1
        if thousands_counter % 1000 == 0:
            print(thousands_counter)

    fig = px.line_geo(lat=lats, lon=lons) #, hover_name=names)
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


def main():
    #first_method()
    second_method()


if __name__ == '__main__':
    main()