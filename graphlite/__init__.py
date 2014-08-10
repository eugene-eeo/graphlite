from graphlite.graph import Graph
from graphlite.query import V


def connect(uri, graphs=()):
    """
    Returns a Graph object with the given URI and
    created graphs.

    :param uri: The URI to the SQLite DB.
    :param graphs: The graphs to create.
    """
    return Graph(uri=uri, graphs=graphs)
