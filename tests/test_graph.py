import pytest
from graphlite import V
from sqlite3 import ProgrammingError


def test_contains(graph):
    assert V(1).knows(2) in graph


def test_close(graph):
    graph.close()
    with pytest.raises(ProgrammingError):
        graph.db.execute('INSERT INTO knows (src,dst) VALUES (1,1)')
