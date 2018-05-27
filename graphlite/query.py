from contextlib import closing
from itertools import islice
from collections import namedtuple
import graphlite.sql as SQL


_V = namedtuple('V', ('src', 'rel', 'dst'))


class V(_V):
    """
    Create a new V object that represents an edge. This
    object is expected throughout the API where the
    parameter is named `edge`. All parameters are optional
    and default to None.

    :param src: The source node.
    :param rel: The relation.
    :param dst: The destination node.
    """

    def __new__(cls, src=None, rel=None, dst=None):
        return _V.__new__(cls, src, rel, dst)

    def __getattr__(self, attr):
        return V(self.src, attr, self.dst)

    def __call__(self, dst):
        """
        Assign a destination node to the edge.

        :param dst: The destination node.
        """
        return V(self.src, self.rel, dst)

    def __repr__(self):
        return '(%s)-[%s]->(%s)' % (
            '*' if self.src is None else self.src,
            '*' if self.rel is None else ':%s' % self.rel,
            '*' if self.dst is None else self.dst,
        )

    def gen_query(self):
        """
        Generate an SQL query for the edge object.
        """
        return (
            SQL.forwards_relation(self.src, self.rel) if self.dst is None else
            SQL.inverse_relation(self.dst, self.rel)
            )


class Query(object):
    __slots__ = ('db', 'sql', 'params')

    """
    Create a new query object that acts on a particular
    SQLite connection instance.

    :param db: The SQLite connection.
    """
    def __init__(self, db, sql=(), params=()):
        self.db = db
        self.sql = sql
        self.params = params

    @property
    def statement(self):
        """
        Joins all of the SQL queries together and then
        returns the result. It is the query to be ran.
        """
        return '\n'.join(self.sql)

    def __iter__(self):
        """
        Execute the internally stored SQL query and then
        yield every result to the caller. You can reuse
        this function as many times as you want but it
        may not return the same values.
        """
        with closing(self.db.cursor()) as cursor:
            cursor.execute(self.statement, self.params)
            for row in cursor:
                yield row[0]

    def derived(self, statement, params=(), replace=False):
        """
        Returns a new query object set up correctly with
        the *statement* and *params* appended to the end
        of the new instance's internal query and params,
        along with the current instance's connection.

        :param statement: The SQL query string to append.
        :param params: The parameters to append.
        :param replace: Whether to replace the entire
            SQL query.
        """
        return Query(
            db=self.db,
            sql=(statement,) if replace else self.sql + (statement,),
            params=self.params + params,
        )

    def __call__(self, edge):
        """
        Selects either destination nodes or source nodes
        based on the edge query provided. If source node
        is specified, then destination nodes are selected,
        and vice versa.

        :param edge: The edge query.
        """
        smt, params = edge.gen_query()
        return self.derived(smt, params)

    def traverse(self, edge):
        """
        Traverse the graph, and selecting the destination
        nodes for a particular relation that the selected
        nodes are a source of, i.e. select the friends of
        my friends. You can traverse indefinitely.

        :param edge: The edge query. If the edge's
            destination node is specified then the source
            nodes will be selected.
        """
        query = self.statement
        rel, dst = edge.rel, edge.dst
        statement, params = (
            SQL.compound_fwd_query(query, rel) if dst is None else
            SQL.compound_inv_query(query, rel, dst)
        )
        return self.derived(statement, params, replace=True)

    @property
    def intersection(self):
        """
        Intersect the current query with another one
        using an SQL INTERSECT.
        """
        return self.derived('INTERSECT')

    @property
    def difference(self):
        """
        Compute the difference between the current
        selected nodes and the another query, and
        not a `symmetric difference`. Similar in
        implementation to
        :meth:`graphlite.query.Query.intersection`.
        """
        return self.derived('EXCEPT')

    @property
    def union(self):
        """
        Compute the union between the current selected
        nodes and another query. Similar to the
        :meth:`graphlite.query.Query.intersection`
        method.
        """
        return self.derived('UNION')

    def count(self):
        """
        Counts the objects returned by the query.
        You will not be able to iterate through this
        query again (with deterministic results,
        anyway).
        """
        return sum(1 for __ in self)

    def __getitem__(self, obj):
        """
        Only supports slicing operations, and returns
        an iterable with the slice taken into account.

        :param obj: The slice object.
        """
        smt, params = SQL.limit(obj.start, obj.stop)
        return islice(
            self.derived(smt, params),
            None,
            None,
            obj.step,
            )

    def to(self, datatype):
        """
        Converts this iterable into another *datatype*
        by calling the provided datatype with the
        instance as the sole argument.

        :param datatype: The datatype.
        """
        return datatype(self)
