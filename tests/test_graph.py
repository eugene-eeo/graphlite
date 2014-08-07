from graphlite import V, Graph
from threading import Thread
from sqlite3 import ProgrammingError


def test_concurrency():
    g = Graph(uri=':memory:', graphs=['knows'])

    def store(value):
        def callback():
            g.store(V(1).knows(value))
        return callback

    stored = (2, 3, 4, 5)
    threads = [Thread(target=store(x)) for x in stored]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    for item in stored:
        assert V(1).knows(item) in g


def test_store(graph):
    graph.store(V(1).knows(10))
    assert V(1).knows(10) in graph


def test_contains(graph):
    assert V(1).knows(2) in graph


def test_delete(graph):
    graph.delete(V(1).knows(4))
    assert not V(1).knows(4) in graph

    graph.delete(V().knows(2))
    assert not V(1).knows(2) in graph

    graph.delete(V().knows)
    assert not V(1).knows(3) in graph


def test_close(graph):
    graph.close()
    try:
        graph.store(V(1).knows(10))
        raise AssertionError
    except ProgrammingError:
        pass
