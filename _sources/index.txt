.. Graphlite documentation master file, created by
   sphinx-quickstart on Sun Aug 10 16:02:03 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Graphlite
====================

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

If you are not familiar or new to the library perhaps you
should check out :doc:`intro`. Else, you are most likely
looking for the :doc:`api`.


.. toctree::
   :maxdepth: 2

   intro
   usage
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

