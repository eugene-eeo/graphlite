![Graphlite](https://raw.github.com/eugene-eeo/graphlite/master/art/logo-300.png)

Graphlite is a tiny graph datastore that stores adjacency lists
similar to FlockDB but like conventional graph databases, allow
you to query them with traversals (graph-walking queries), and
works with datasets that you can fit into your SQLite database.

```python
from graphlite import connect, V
graph = connect(':memory:', graphs=['knows'])

with graph.transaction() as tr:
    for i in range(2, 5):
        tr.store(V(1).knows(i))
    tr.store(V(2).knows(3))
    tr.store(V(3).knows(5))

# who are the friends of friends of
# both 1 and 2?
graph.find(V(1).knows)\
     .intersection(V(2).knows)\
     .traverse(V().knows)
```

Graphlite is thread safe, meaning that when transactions are
comitted (at the end of the `with` block), a lock is held and
only the thread that commits gets to run. Thread safety is
emphasised if you look at the test suite.

The library is currently under construction and API changes are
unevitable until it's released on PyPI. Currently I'm working
on stabilising the API so we can hit 1.0 as soon as possible.

## Contributing

If you want to contribute, we follow the Github workflow, so
fork the repo, work on the code and just make a pull request
(make sure all tests pass beforehand, at least in the last
commit of your pull request). In short:

```sh
$ git clone ssh://git@github.com/eugene-eeo/graphlite.git
$ cd graphlite
$ git checkout -b $FEATURE
$ # hackedy hack hack
$ py.test
$ git commit -a
$ git push
```

Note that we use `py.test` for testing so if you haven't, make
sure you `pip install pytest`. But you should.


* **Code status**: ![Build](https://img.shields.io/travis/eugene-eeo/graphlite.svg)
* **Maintainer**: [Eugene Eeo](https://github.com/eugene-eeo)
* **License**: MIT
