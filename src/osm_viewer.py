import plotly.graph_objects as go


def create_map_view():
    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = [23.7412804,23.7483916,23.7551121],
        lat = [38.0331949,38.0347879,38.0380574],
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


def main():
    fig = create_map_view()
    fig.show()


if __name__ == '__main__':
    main()