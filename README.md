![graphlite](https://raw.github.com/eugene-eeo/graphlite/master/art/logo-300.png)


![Build Stats](http://img.shields.io/travis/eugene-eeo/graphlite.svg)

A simple MIT-licensed social graph datastore using the SQLite
library as a backend. Graphlite provides storage for nodes-
unsigned integers that represent objects in another datastore,
for example the ID of your users and their posts.

```python
from graphlite import Graph, V
g = Graph(uri=':memory:', graphs=['follows'])

with g.transaction() as tr:
    for i in range(2, 5):
        tr.store(V(1).knows(i))
```

The relations, when stored in the SQLite database, are not
indexed by their recency or any time based value, but rather
by either the source or destination nodes. All queries are
performed using these clustered indexes as well.

Graphlite aims to be performant and sane, as well as offering
a nice API for developers to work with. I also aim for the
library being thread-safe. Being inspired by FlockDB, Graphlite
supports both simple and compound arithmetic queries, as well
as queries to forwards and backwards relations:

```python
g.find(V(1).knows)
g.find(V(1).knows).intersection(...)
g.find(V(1).knows).difference(...)
g.find(V().knows(1)).union(...)
```

They are pretty self explanatory. You can use them to simulate
graph traversal, although for some edge cases you may need the
slower `traverse` method:

```python
g.find(V(1).knows).traverse(V().knows)
g.find(V(1).knows).traverse(...).traverse(...)
```

I.e. for unavoidable situations to find out who does the people
that 1 knows, know. Like regular Python collections you can also
slice the results, i.e.:

```python
g.find(V(1).knows)[2:10]
g.find(V(3).knows)[1::2]
```

Sometimes just validating relations is what you want.

```python
if V(1).knows(2) in g:
    # HE HAS A FRIEND!
```

If you are looking for a package that can scale up with SQLite
and is simple to work with, while sane, then Graphlite is for
you. Else I recommend you to start looking at various other
libraries like [neomodel](https://github.com/robinedwards/neomodel),
or the Python interface to the FlockDB database, if you are into
adjacency lists: [python-flockdb](https://github.com/pyronicide/python-flockdb).
