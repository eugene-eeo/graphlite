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

When your generator gets too large, it is often better to use the
:meth:`graphlite.transaction.Transaction.store_many` method because
it's more efficient in terms of space:

.. code-block:: python

    with graph.transaction() as tr:
        tr.store_many(V(1).knows(n) for n in range(2, 200))

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

And you can also specify the destination node to the ``traverse``
query to select the source nodes that have the specific relation
to the destination node. For example, to select the friends of friends
of 1 that are friends with 2:

.. code-block:: python

    graph.find(V(1).knows).traverse(V().knows(2))

Perhaps you want to keep traversing and find out the friends of those
people? You can do that as well:

.. code-block:: python

    graph.find(V(1).knows).traverse(V().knows(2))\
                          .traverse(V().knows)

You can also slice the query objects the same way you'd slice a slice
object, but you will only get an iterable back. For example to get the
first five people that 1 knows:

.. code-block:: python

    graph.find(V(1).knows)[:5]

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

Similar to :meth:`graphlite.transaction.Transaction.store_many`
method, you should use the :meth:`graphlite.transaction.Transaction.delete_many`
method if you are deleting many specific nodes at once. For
example:

.. code-block:: python

    with graph.transaction() as tr:
        tr.delete_many(V(1).knows(i) for i in gen())

Note that transactions are not locked, in a sense that the
code within the ``with`` block is not ran in a thread lock.
The lock will only be held during block exit, which is also
when the transaction will be committed.
