from contextlib import closing
from sqlite3 import Connection

import graphlite.sql as SQL
from graphlite.query import Query


class Graph(object):
    def __init__(self, uri, graphs=[]):
        self.uri = uri
        self.db = Connection(
            database=uri,
            check_same_thread=False,
            isolation_level=None
        )
        self.setup_sql(graphs)

    def setup_sql(self, graphs):
        with closing(self.db.cursor()) as cursor:
            for item in graphs:
                cursor.execute(SQL.CREATE_TABLE % (item))
                for index in SQL.INDEXES:
                    cursor.execute(index % (item))
            self.db.commit()

    def close(self):
        self.db.close()

    def store(self, edge):
        with closing(self.db.cursor()) as cursor:
            cursor.execute(*SQL.store(edge.src, edge.rel, edge.dst))
            self.db.commit()

    def delete(self, edge):
        with closing(self.db.cursor()) as cursor:
            cursor.execute(*SQL.remove(edge.src, edge.rel, edge.dst))
            self.db.commit()

    def exists(self, edge):
        with closing(self.db.cursor()) as cursor:
            cursor.execute(*SQL.select_one(edge.src, edge.rel, edge.dst))
            return bool(tuple(cursor))

    @property
    def find(self):
        return Query(self.db)
