Introduction to Graphlite
=========================

------------------
What is Graphlite?
------------------

Graphlite is a social graph datastore. It doesn't store
properties between relations, but it can store thousands
of relations between integers, which are most likely
representing objects in your other databases, such as
the ID column of your users/statuses table.

Being based on a relational DBM, Graphlite supports very
atomic transactions, similar to the transactions that
SQLite offers even with transactions, performance isn't
degraded because the SQLite library is very, very fast.

Graphlite aims to be performant, thread safe, and have
a pleasant API for developer happiness. For example, to
create a transaction:

.. code-block:: python

    with graph.transaction() as tr:
        for item in range(2, 6):
            tr.store(V(1).knows(item))

And one thing I'm very happy with is how querying works
and the expressiveness of the querying "syntax":

.. code-block:: python

    graph.find(V(1).knows)\
         .union(V(3).knows)\
         .traverse(V().posted)

----------
Cheatsheet
----------

To connect to an existing SQLite database file (substitute
``URI`` and ``GRAPHS`` with the URI of your database file
and the graphs that you want to query/insert to):

.. code-block:: python

    from graphlite import connect, V
    graph = connect(URI, graphs=GRAPHS)

To insert (possibly multiple) relation(s), you must create
a transaction and call methods of the transaction object:

.. code-block:: python

    with graph.transaction() as tr:
        tr.store(V(1).knows(2))

To query the graph, you can simply do:

.. code-block:: python

    graph.find(V(1).knows)   # people that 1 knows
    graph.find(V().knows(1)) # people that knows 1

Querying has a few more "tricks", notably the powerful set
operations that you can do:

.. code-block:: python

    graph.find(...).union(...)
    graph.find(...).difference(...)
    graph.find(...).intersection(...)

They should be quite familiar to you (remember the Venn
diagrams from school?). If you are not familiar with set
operations or would like a demo of how they work I would
recommend looking at `this <http://www.texample.net/media/tikz/examples/PNG/set-operations-illustrated-with-venn-diagrams.png>`_
diagram.

Graphlite also supports "graph-hopping" or graph traversal
queries, in spite of the fact that it was inspired by
FlockDB:

.. code-block:: python

    graph.find(V(1).knows).traverse(V().knows)

The above query states that "find all of the people that 1
knows, and then find all of the people that `they` know".
You can also pass in a destination node to the second query,
to select the source nodes:

.. code-block:: python

    graph.find(V(1).knows).traverse(V().knows(2))

Which means "find all of the people that one knows, that
knows 2". This can also be expressed with the help of an
intersection:

.. code-block:: python

    graph.find(V(1).knows).intersection(V().knows(2))

Note that you can traverse indefinitely, i.e. to find out
who are the friends of friends of the people that know 2,
you can do:

.. code-block:: python

    graph.find(V().knows(2)).traverse(V().knows)\
                            .traverse(V().knows)

You can also count the nodes returned by a query via the
``count`` method:

.. code-block:: python

    graph.find(V(1).knows).count()

To delete edges from the datastore, you have three options:

- Specific deletes
- Inverse & Forwards deletes
- Relation-wide deletes

To illustrate,

.. code-block:: python

    with graph.transaction() as tr:
        tr.delete(V(1).knows(2))
        # delete edges of type "1 knows ..."
        tr.delete(V(1).knows)

        # delete edges of type "... knows 1"
        tr.delete(V().knows(2))

        # delete edges of type "... knows ..."
        tr.delete(V().knows)

