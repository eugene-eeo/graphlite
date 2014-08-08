from graphlite import V, Graph
from threading import Thread
from sqlite3 import ProgrammingError


def test_contains(graph):
    assert V(1).knows(2) in graph


def test_close(graph):
    graph.close()
    try:
        graph.db.execute('INSERT INTO knows (src,dst) VALUES (1,1)')
        raise AssertionError
    except ProgrammingError:
        pass
