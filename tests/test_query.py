from graphlite import V


def test_find(graph):
    assert list(graph.find(V(1).knows)) == [2, 3, 4]
    assert list(graph.find(V().knows(1))) == [2, 3]


def test_union(graph):
    assert list(graph.find(V(1).knows)
                     .union(V(2).knows)) == [1, 2, 3, 4]


def test_intersection(graph):
    assert list(graph.find(V(1).knows)
                     .intersection(V().knows(1))) == [2, 3]


def test_difference(graph):
    assert list(graph.find(V(1).knows)
                     .difference(V().knows(1))) == [4]


def test_traverse(graph):
    assert list(graph.find(V(1).knows)
                     .traverse(V().knows)) == [1, 1]
    assert list(graph.find(V(1).knows)
                     .traverse(V().knows(1))) == [2, 3]


def test_count(graph):
    assert graph.find(V(1).knows).count() == 3
    assert graph.find(V(1).likes).count() == 2


def test_slice(graph):
    assert len(list(graph.find(V(1).knows)[:1])) == 1
    assert list(graph.find(V(1).knows)[1:]) == [3, 4]
