from graphlite.graph import Graph
from graphlite.query import V


def connect(uri, graphs=()):
    return Graph(uri=uri, graphs=graphs)
