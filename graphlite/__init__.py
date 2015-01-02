"""
    graphlite
    ~~~~~~~~~
    A pure-Python embedded graph datastore built on
    top of SQLite.

    :copyright: (c) 2014-2015 by Eugene Eeo.
    :license: MIT, see LICENSE for more details.
"""


from graphlite.graph import Graph
from graphlite.query import V


def connect(uri, graphs=()):
    """
    Returns a Graph object with the given *uri* and
    created *graphs*.

    :param uri: The URI to the SQLite DB.
    :param graphs: The graphs to create.
    """
    return Graph(uri, graphs)
