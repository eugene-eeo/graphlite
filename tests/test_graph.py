from graphlite import V, Graph
from threading import Thread
from sqlite3 import ProgrammingError, OperationalError


def threading_test(function, iterable):
    threads = [Thread(target=function(x)) for x in iterable]

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


def test_store_multiple(graph):
    edges = [V(1).knows(i) for i in range(5, 10)]
    graph.store_multiple(edges)

    for item in edges:
        assert item in graph

    try:
        graph.store_multiple([V(1).knows(11), V(1).do(2)])
        raise AssertionError
    except OperationalError:
        assert V(1).knows(11) not in graph


def test_concurrent_store_multiple():
    g = Graph(uri=':memory:', graphs=['knows'])

    def store(iterable):
        def callback():
            g.store_multiple(iterable)
        return callback

    stored = ([V(1).knows(2), V(1).knows(5)], [V(1).knows(3), V(1).knows(4)])
    threading_test(store, stored)

    for item in stored:
        for edge in item:
            assert edge in g


def test_concurrency():
    g = Graph(uri=':memory:', graphs=['knows'])

    def store(value):
        def callback():
            g.store(V(1).knows(value))
        return callback

    stored = (2, 3, 4, 5)
    threading_test(store, stored)

    for item in stored:
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
