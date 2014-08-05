from contextlib import closing
import graphlite.sql as SQL


class V(object):
    __slots__ = ('src', 'rel', 'dst')

    """
    Create a new V object that represents an edge. This
    object is expected throughout the API where the
    parameter is named `edge`.
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


class Query(object):
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
        src, rel, dst = edge.src, edge.rel, edge.dst
        statement, params = (
            SQL.forwards_relation(src, rel) if dst is None else
            SQL.inverse_relation(dst, rel)
        )
        self.sql.append(statement)
        self.params.extend(params)
        return self

    def traverse(self, edge):
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
        self.sql.append('INTERSECT')
        return self

    @property
    def difference(self):
        self.sql.append('EXCEPT')
        return self

    @property
    def union(self):
        self.sql.append('UNION')
        return self

    def count(self):
        return sum(1 for __ in self)

    def limit(self, count):
        self.sql.append('LIMIT %d' % (count))
        return self
