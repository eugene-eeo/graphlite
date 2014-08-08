# <img src="https://raw.github.com/eugene-eeo/graphlite/master/art/logo-300.png">

![Build](https://img.shields.io/travis/eugene-eeo/graphlite.svg)

### Relations, simplified

**Graphlite** is a social graph interface over SQLite for
relatively small datasets. It can handle anything that the
underlying SQLite backend can cope with.


## Usage

**Graphlite** was designed to be as minimal and modular
as possible, and as performant as possible, while at the
same time be as developer friendly as possible. It does
not aim to solve lots of problems, but rather be good at
solving specific problems. The internal codebase was also
designed around reusability and the components concept-
we can swap one database driver out for another if needed.

Start by initializing a new graph in a URI:

```python
from graphlite import V, connect
graph = connect(':memory:', graphs=['follows'])
```

Note that you need to pass an iterable to the function-
this is because **Graphlite** needs to know which relations
you are going to write to or read from. Rule of thumb:
if the call modifies the graph, you'll have to use a
transaction:

```python
with graph.transaction() as tr:
    for i in range(2, 4):
        tr.store(V(1).knows(i))

assert V(1).knows(2) in graph
assert V(1).knows(3) in graph
```

Then perform queries on your data- you can either perform
forwards (where the source node is specified and you want
to select the destination node), or inverse (the opposite
of forwads) queries:

```python
graph.find(V(1).knows)
graph.find(V().knows(1))
```

And similar to FlockDB, **Graphlite** also offers powerful
set-based operations to be performed against queries:

```python
graph.find(...).intersection(...)
graph.find(...).difference(...)
graph.find(...).union(...)
```

A feature inspired from the MongoEngine ORM is counting and
slicing, which gives rise to powerful queries:

```python
graph.find(...).count()
graph.find(...)[:5]
```

Of course, traversal operations are also supported by the
library. Even nested traversals are possible, for example,
to get the people that 1's friends knows that knows 2, we
can do the following query:

```python
friends = graph.find(V(1).knows).traverse(V().knows)
friends.traverse(V().knows(2))
```

Powerful deletes are also possible, though if you need
more than simple forwards/inverse/relation-only queries
then you will have to do specific deletes.

```python
with graph.transaction() as tr:
    tr.delete(V(1).knows(2))
    tr.delete(V(1).knows)
    tr.delete(V().knows(2))

    # deletes the entire table
    tr.delete(V().knows)
```
