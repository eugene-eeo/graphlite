from graphlite import V
from graphlite.transaction import AbortSignal
from sqlite3 import OperationalError
from threading import Thread


def threading_test(function, iterable):
    threads = [Thread(target=function(x)) for x in iterable]

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


def test_concurrency(graph):
    stored = [V(1).knows(i) for i in range(5, 9)]

    def store(value):
        def callback():
            with graph.transaction() as tr:
                tr.store(value)
        return callback

    threading_test(store, stored)
    for item in stored:
        assert item in graph


def test_delete(graph):
    queries = [
        V(1).knows(2),
        V().knows(3),
        V().knows,
    ]
    assertions = [
        lambda: V(1).knows(2) not in graph,
        lambda: V(1).knows(3) not in graph,
        lambda: V(1).knows(4) not in graph,
    ]

    for assertion, query in zip(assertions, queries):
        with graph.transaction() as tr:
            tr.delete(query)
        assert assertion()


def test_transaction(graph):
    with graph.transaction() as tr:
        tr.store(V(1).knows(7))
        tr.store(V(1).knows(8))

    assert V(1).knows(7) in graph
    assert V(1).knows(8) in graph


def test_transaction_atomic(graph):
    try:
        with graph.transaction() as tr:
            tr.store(V(1).knows(7))
            tr.store(V(1).does(1))
        raise AssertionError
    except OperationalError:
        assert V(1).knows(7) not in graph


def test_transaction_abort(graph):
    with graph.transaction() as tr:
        tr.store(V(1).knows(10))
        tr.abort()

    assert V(1).knows(10) not in graph


def test_transaction_multiple(graph):
    to_delete = (2, 3, 4)
    to_store = (6, 7, 8)

    with graph.transaction() as tr:
        tr.store_many(V(1).knows(n) for n in to_store)
        tr.delete_many(V(1).knows(n) for n in to_delete)

    for deleted, stored in zip(to_delete, to_store):
        assert V(1).knows(deleted) not in graph
        assert V(1).knows(stored) in graph
