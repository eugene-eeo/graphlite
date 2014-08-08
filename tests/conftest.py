import pytest
from graphlite import Graph, V


@pytest.fixture
def graph(request):
    g = Graph(uri=':memory:',
              graphs=['likes', 'knows'])

    with g.transaction() as tr:
        for i in range(2, 5):
            tr.store(V(1).knows(i))
            if i != 4:
                tr.store(V(1).likes(i))
                tr.store(V(i).knows(1))

    request.addfinalizer(lambda: g.close())
    return g
