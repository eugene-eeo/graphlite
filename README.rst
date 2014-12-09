.. image:: https://raw.github.com/eugene-eeo/graphlite/master/art/logo.png
   :alt: Graphlite

|Build| |Downloads|

Graphlite is an MIT-licensed graph DB for Python.

There are currently no embedded graph databases for Python.
Graphlite aims to change that by building a simple and fast
graph layer over SQLite. Similar to FlockDB, Graphlite only
stores adjacency lists, but they can be queried in the style
of normal graph databases, e.g. with traversals.

.. code-block:: pycon

    >>> import graphlite as g
    >>> db = g.connect(':memory:')

    >>> with db.transaction():
    ...     for person in [2, 3]:
    ...         db.store(g.V(1).knows(person))
    ...

    >>> db.find(g.V(1).knows).to(list)
    [2, 3]

Graphlite inherits it's API from that of FlockDB's. Also, like
FlockDB Graphlite only stores the relations between the nodes,
which are integers- not the data of the nodes themselves. You
will therefore need a high performance database like BerkleyDB
or one of the **dbm** implementations to store your data.


Features
--------

- Thread-safe transactions with **threading.Lock**
- Small, easy to learn API with around 100% coverage
- Lazy generator based API when querying
- Highly documented codebase


Installation
------------

To install Graphlite, simply::

    $ pip install graphlite


.. |Build| image:: https://img.shields.io/travis/eugene-eeo/graphlite.svg
   :target: https://travis-ci.org/eugene-eeo/graphlite/
.. |Downloads| image:: https://img.shields.io/pypi/dm/graphlite.svg
   :target: https://pypi.python.org/pypi/graphlite
