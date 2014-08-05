import pytest
from graphlite import Graph, V


@pytest.fixture
def graph(request):
    g = Graph(uri=':memory:',
              graphs=['likes', 'knows'])

    for i in range(2, 5):
        g.store(V(1).knows(i))
        if i != 4:
            g.store(V(1).likes(i))
            g.store(V(i).knows(1))

    request.addfinalizer(lambda: g.close())
    return g
