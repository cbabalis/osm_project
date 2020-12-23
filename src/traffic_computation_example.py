import traffic_computation as tc


def main():
    graph = tc.create_graph_from_osm_place('Athens', simplify=True)
    nodes, edges = ox.graph_to_gdfs(graph)
    traffic_edges = populate_network_traffic(edges, start1, end1, start2, end2)
    some_rows = split_osmid_field(traffic_edges)
    len(some_rows)
    loaded_edges_df = pd.concat(some_rows)
    print(len(loaded_edges_df))
    loaded_edges_df.to_csv('loaded_edges.csv')


if __name__ == '__main__':
    main()