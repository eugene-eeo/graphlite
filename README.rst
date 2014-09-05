.. image:: https://raw.github.com/eugene-eeo/graphlite/master/art/logo-300.png
   :alt: Graphlite

Graphlite is a tiny graph datastore that stores adjacency lists
similar to FlockDB but like conventional graph databases, allow
you to query them with traversals (graph-walking queries), and
works with datasets that you can fit into your SQLite database.

.. code-block:: python

    from graphlite import connect, V
    graph = connect(':memory:', graphs=['knows'])

    with graph.transaction() as tr:
        for i in range(2, 5):
            tr.store(V(1).knows(i))
        tr.store(V(2).knows(3))
        tr.store(V(3).knows(5))

    # who are the friends of the mutual friends
    # of both 1 and 2?
    graph.find(V(1).knows)\
         .intersection(V(2).knows)\
         .traverse(V().knows)

Graphlite is thread safe, meaning that when transactions are
comitted (at the end of the ``with`` block), a lock is held and
only the thread that commits gets to run. Thread safety is
emphasised if you look at the test suite.

----------
Installing
----------

.. code-block:: sh

    $ pip install graphlite

------------
Contributing
------------

If you want to contribute, we follow the Github workflow, so
fork the repo, work on the code and just make a pull request
(make sure all tests pass beforehand, at least in the last
commit of your pull request). In short:

.. code-block:: sh

    $ git clone ssh://git@github.com/$USERNAME/graphlite.git
    $ cd graphlite
    $ git checkout -b $FEATURE
    $ # hackedy hack hack
    $ py.test tests
    $ git commit -a
    $ git push

Note that we use ``py.test`` for testing so if you haven't,
make sure you ``pip install pytest``. But you should.


* **Code status**: |Build|
* **Maintainer**: `Eugene Eeo`_
* **License**: MIT

.. |Build| image:: https://img.shields.io/travis/eugene-eeo/graphlite.svg?style=flat
    :target: https://travis-ci.org/eugene-eeo/graphlite/
.. _Eugene Eeo: http://github.com/eugene-eeo
