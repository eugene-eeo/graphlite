import pytest
from graphlite import connect, V


@pytest.fixture
def graph(request):
    g = connect(':memory:', graphs=['likes', 'knows'])

    with g.transaction() as tr:
        # 1 knows 2,3,4
        # 2,3 knows 1
        # 1 likes 2,3
        for i in (2, 3, 4):
            tr.store(V(1).knows(i))
            if i != 4:
                tr.store(V(i).knows(1))
                tr.store(V(1).likes(i))

    request.addfinalizer(g.close)
    return g
