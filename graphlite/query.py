from contextlib import closing
from itertools import islice
import graphlite.sql as SQL


class V(object):
    __slots__ = ('src', 'rel', 'dst')

    """
    Create a new V object that represents an edge. This
    object is expected throughout the API where the
    parameter is named `edge`. All parameters are optional
    and default to None.

    :param src: The source node.
    :param rel: The relation.
    :param dst: The destination node.
    """
    def __init__(self, src=None, rel=None, dst=None):
        self.src = src
        self.rel = rel
        self.dst = dst

    def __getattr__(self, attr):
        values = self.__slots__
        if attr in values:
            return values[attr]
        self.rel = attr
        return self

    def __call__(self, dst):
        """
        Assign a destination node to the edge.

        :param dst: The destination node.
        """
        self.dst = dst
        return self

    def __repr__(self):
        return '(%s)-[%s]->(%s)' % (
            '*' if self.src is None else self.src,
            '*' if self.rel is None else ':%s' % (self.rel),
            '*' if self.dst is None else self.dst
        )

    def __eq__(self, other):
        if not isinstance(other, V):
            return False
        return (self.src == other.src and
                self.rel == other.rel and
                self.dst == other.dst)

    def __hash__(self):
        return hash((self.src, self.rel, self.dst))


class Query(object):
    """
    Create a new query object that acts on a particular
    SQLite connection instance.

    :param db: The SQLite connection.
    """
    def __init__(self, db):
        self.db = db
        self.sql = []
        self.params = []

    def __iter__(self):
        statement = '\n'.join(self.sql)
        with closing(self.db.cursor()) as cursor:
            cursor.execute(statement, self.params)
            for item in cursor:
                yield item[0]

    def __call__(self, edge):
        """
        Selects either destination nodes or source nodes
        based on the edge query provided. If the source
        node is specified in the edge query then the
        destination nodes will be selected, else the
        source nodes will be selected. Note that either
        one of the source or destination nodes (but not
        necessarily both) must be specified in the edge
        query.

        :param edge: The edge query.
        """
        src, rel, dst = edge.src, edge.rel, edge.dst
        statement, params = (
            SQL.forwards_relation(src, rel) if dst is None else
            SQL.inverse_relation(dst, rel)
        )
        self.sql.append(statement)
        self.params.extend(params)
        return self

    def traverse(self, edge):
        """
        Traverse the graph, and selecting the destination
        nodes for a particular relation that the selected
        nodes are a source of. I.e. select the friends of
        my friends.

        :param edge: The edge object. If the edge's
        destination node is specified then the source
        nodes will be selected.
        """
        query = '\n'.join(self.sql)
        rel, dst = edge.rel, edge.dst
        statement, params = (
            SQL.compound_fw_query(rel, query) if dst is None else
            SQL.compound_iv_query(dst, rel, query)
        )
        self.sql = [statement]
        self.params.extend(params)
        return self

    @property
    def intersection(self):
        """
        Returns the Query object itself but inserts a
        SQL intersection keyword.
        """
        self.sql.append('INTERSECT')
        return self

    @property
    def difference(self):
        """
        Similar to the :meth:``Query.intersection``
        method, but sets up the query object for an
        SQL ``EXCEPT`` query.
        """
        self.sql.append('EXCEPT')
        return self

    @property
    def union(self):
        """
        Similar to the :meth:``Query.intersection``
        method and sets up the query object for a
        UNION query.
        """
        self.sql.append('UNION')
        return self

    def count(self):
        """
        Counts the objects returned by the query.
        You will not be able to iterate through this
        query again (with deterministic results,
        anyway).
        """
        return sum(1 for __ in self)

    def __getitem__(self, value):
        return islice(self, value.start, value.stop, value.step)
