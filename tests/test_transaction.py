import pytest
from graphlite import V
from graphlite.transaction import AbortSignal
from sqlite3 import OperationalError
from threading import Thread


def test_transaction_concurrency(graph):
    stored = [V(1).knows(i) for i in range(5, 9)]

    def store(value):
        def callback():
            with graph.transaction() as tr:
                tr.store(value)
        return callback

    threads = [Thread(target=store(x)) for x in stored]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    for item in stored:
        assert item in graph


def test_transaction_delete(graph):
    queries = [
        V(1).knows(2),
        V(1).likes,
        V().knows(3),
        V().knows,
    ]
    edges = [
        V(1).knows(2),
        V(1).likes(2),
        V(1).knows(3),
        V(1).knows(4),
    ]

    for edge, query in zip(edges, queries):
        with graph.transaction() as tr:
            tr.delete(query)
        assert edge not in graph


def test_transaction_store(graph):
    with graph.transaction() as tr:
        tr.store(V(1).knows(7))
        tr.store(V(1).knows(8))

    assert V(1).knows(7) in graph
    assert V(1).knows(8) in graph


def test_transaction_atomic(graph):
    with pytest.raises(OperationalError):
        with graph.transaction() as tr:
            tr.store(V(1).knows(7))
            tr.store(V(1).does(1))

    assert V(1).knows(7) not in graph


def test_transaction_abort(graph):
    with graph.transaction() as tr:
        tr.store(V(1).knows(10))
        tr.abort()

    assert V(1).knows(10) not in graph


def test_transaction_nested(graph):
    with pytest.raises(OperationalError):
        with graph.transaction() as tr1:
            with graph.transaction() as tr2:
                tr2.store(V(1).does(2))
            tr1.store(V(1).knows(5))

    assert V(1).knows(5) not in graph


def test_transaction_many(graph):
    to_delete = (2, 3, 4)
    to_store = (6, 7, 8)

    with graph.transaction() as tr:
        tr.store_many(V(1).knows(n) for n in to_store)
        tr.delete_many(V(1).knows(n) for n in to_delete)

    for deleted, stored in zip(to_delete, to_store):
        assert V(1).knows(deleted) not in graph
        assert V(1).knows(stored) in graph


def test_transaction_isolation(graph):
    with graph.transaction() as tr:
        tr.store(V(1).knows(5))
        assert V(1).knows(5) not in graph
