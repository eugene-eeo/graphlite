from graphlite.graph import Graph
from graphlite.query import V


def connect(uri, *args, **kwargs):
    return Graph(uri=uri, *args, **kwargs)
