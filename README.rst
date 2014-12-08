.. image:: https://raw.github.com/eugene-eeo/graphlite/master/art/logo-300.png
   :alt: Graphlite

|Build| |Downloads|

Graphlite is an MIT-licensed embedded graph datastore for Python
built on top of SQLite. It stores adjacency lists but allows for
traversals and works with whatever dataset that you can fit into
an SQLite DB.

.. code-block:: pycon

    >>> import graphlite as g
    >>> db = g.connect(':memory:')

    >>> with db.transaction():
    ...     for person in [2, 3]:
    ...         db.store(g.V(1).knows(person))
    ...

    >>> db.find(g.V(1).knows).to(list)
    [2, 3]

Graphlite inherits it's API from that of FlockDB's. It doesn't
provide any method for storing an object into the database, but
only supports retrieving and storing integers (nodes) which can
mean anything in the context of your application.


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
