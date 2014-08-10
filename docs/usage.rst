Usage
=====

**Note:** If you have read through the cheatsheet then this document
for you, will just go deeper into the internals of Graphlite.


----------------------
Initializing the graph
----------------------

To initialize a graph object, you have two options- using the
:class:`graphlite.graph.Graph` object or the :meth:`graphlite.connect`
function. Usually you would use :meth:`graphlite.connect` because
it encapsulates anything that the codebase would want to do in
the future.

.. code-block:: python

    from graphlite import V, connect
    graph = connect(':memory:', graphs=['knows'])

Note that since Graphlite is based internally on SQLite (in fact
it can be thought as a minimal wrapper around SQLite to give you
a graph layer), you will need to pass in the graphs that you want
to create and query because the appropriate tables need to be
created.


---------------
Inserting edges
---------------

Graphlite represents edges as a row which contains a source node,
a destination node, which is where the source node is "pointing
to", i.e. in the edge "John knows Don", John is the source node
and Don is the destination node. Graphlite also stores the nodes
as unsigned integers, so you will need a separate backing store
to store the documents, i.e. key-value.

.. code-block:: python

    with graph.transaction() as tr:
        for item in range(2, 5):
            tr.store(V(1).knows(item))
        tr.store(V(3).knows(1))
        tr.store(V(2).knows(6))
        tr.store(V(6).knows(7))

**Tip:** anything that modifies the graph (i.e. storage, removal)
will be done within a transaction. This is partially because
Graphlite is based on an SQLite backend and implementing transactions
are quite straightforward this way.

Transactions are automatically committed at the end of the ``with``
block, so you don't have to hold a lock throughout the entirety of
the block.


--------
Querying
--------

Querying can come in two flavours- you either do a forwards query,
where you select the destination nodes and specify the source node,
or an inverse query, where you get the source nodes but specify the
destination node. Again, best explained by example:

.. code-block:: python

    >>> list(graph.find(V(1).knows()))
    [2, 3, 4]
    >>> list(graph.find(V().knows(1)))
    [3]

You can also do queries which involve set operations, i.e. unions,
differences, and intersections. They are all very efficient and
does not require any data processing on our (Graphlite's) side
because they can be represented easily by set operations. Possible
queries:

.. code-block:: python

    graph.find(...).intersection(...)
    graph.find(...).difference(...)
    graph.find(...).union(...)

Graph traversal queries are also possible via Graphlite. For example
to select the friends of friends of 1:

.. code-block:: python

    graph.find(V(1).knows).traverse(V().knows)


--------------
Deleting Edges
--------------

Deleting edges can come in four flavours- you either do a specific
delete of a specific edge, a forwards query, then delete all the
rows (edges) matching it, an inverse query, or just wipe out everything
from the table. Either way, an example would illustrate it best:

.. code-block:: python

    with graph.transaction() as tr:
        tr.delete(V(1).knows(2))

        # every edge with source node 1
        tr.delete(V(1).knows)

        # every edge with destination node 2
        tr.delete(V().knows(2))

        # everything within the knows table
        tr.delete(V().knows)
