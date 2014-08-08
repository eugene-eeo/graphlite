from graphlite import V, Graph
from threading import Thread
from sqlite3 import ProgrammingError, OperationalError


def threading_test(function, iterable):
    threads = [Thread(target=function(x)) for x in iterable]

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


def test_delete_concurrent(graph):
    nodes = list(graph.find(V(1).knows))

    def delete(value):
        def callback():
            graph.delete(V(1).knows(value))
        return callback

    threading_test(delete, nodes)
    for item in nodes:
        assert V(1).knows(item) not in graph


def test_concurrency():
    g = Graph(uri=':memory:', graphs=['knows'])

    def store(value):
        def callback():
            g.store(V(1).knows(value))
        return callback

    nodes = (2, 3, 4, 5)
    threading_test(store, nodes)

    for item in nodes:
        assert V(1).knows(item) in g


def test_store(graph):
    graph.store(V(1).knows(10))
    assert V(1).knows(10) in graph


def test_contains(graph):
    assert V(1).knows(2) in graph


def test_delete(graph):
    graph.delete(V(1).knows(4))
    assert V(1).knows(4) not in graph

    graph.delete(V().knows(2))
    assert V(1).knows(2) not in graph

    graph.delete(V().knows)
    assert V(1).knows(3) not in graph


def test_close(graph):
    graph.close()
    try:
        graph.store(V(1).knows(10))
        raise AssertionError
    except ProgrammingError:
        pass
