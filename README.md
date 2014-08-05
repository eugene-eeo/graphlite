![graphlite](https://raw.github.com/eugene-eeo/graphlite/master/art/logo-300.png)

![Build Stats](https://travis-ci.org/eugene-eeo/graphlite.svg?branch=master)

A simple social graph datastore using the SQLite library as
a backend. Graphlite provides storage for nodes- unsigned
integers that represent objects in another datastore, for
example the ID of your users and their posts.

```
from graphlite import Graph, V
g = Graph(uri=':memory:', graphs=['follows'])

g.store(V(1).knows(2))
g.store(V(1).knows(3))
g.store(V(2).knows(4))
```

The relations, when stored in the SQLite database, are not
indexed by their recency or any time based value, but rather
by either the source or destination nodes. All queries are
performed using these clustered indexes as well.

Graphlite aims to be performant and sane, as well as offering
a nice API for developers to work with. I also aim for the
library being thread-safe. Being inspired by FlockDB, Graphlite
supports both simple and compound arithmetic queries:

```
g.find(V(1).knows)
g.find(V(1).knows).intersection(...)
g.find(V(1).knows).difference(...)
g.find(V(1).knows).union(...)
```

They are pretty self explanatory. You can use them to simulate
graph traversal, although for some edge cases you may need the
slower `traverse` method:

```
g.find(V(1).knows).traverse(V().knows)
```

I.e. for unavoidable situations to find out who does the people
that 1 know, know.
