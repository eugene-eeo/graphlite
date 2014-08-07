from contextlib import closing
from sqlite3 import Connection
from threading import Lock

import graphlite.sql as SQL
from graphlite.query import Query


class Graph(object):
    """
    Initializes a new Graph object.

    :param uri: The URI of the SQLite file.
    :param graphs: Graphs to create.
    """
    def __init__(self, uri, graphs=[]):
        self.uri = uri
        self.db = Connection(
            database=uri,
            check_same_thread=False,
            isolation_level=None
        )
        self.lock = Lock()
        self.setup_sql(graphs)

    def setup_sql(self, graphs):
        """
        Sets up the SQL tables for the graph object,
        and creates indexes as well.

        :param graphs: The graphs to create.
        """
        with closing(self.db.cursor()) as cursor:
            for item in graphs:
                cursor.execute(SQL.CREATE_TABLE % (item))
                for index in SQL.INDEXES:
                    cursor.execute(index % (item))
            self.db.commit()

    def close(self):
        """
        Close the SQLite connection.
        """
        self.db.close()

    def store(self, edge):
        """
        Store an edge in the database.

        :param edge: The edge to store.
        """
        with self.lock:
            with closing(self.db.cursor()) as cursor:
                cursor.execute(*SQL.store(edge.src, edge.rel, edge.dst))
                self.db.commit()

    def delete(self, edge):
        """
        Deletes an edge from the database. Either the source
        node or destination node may be specified- if they
        are not then they won't be taken into account when
        deleting from the relation.

        :param edge: The edge to delete.
        """
        with self.lock:
            with closing(self.db.cursor()) as cursor:
                cursor.execute(*SQL.remove(edge.src, edge.rel, edge.dst))
                self.db.commit()

    def exists(self, edge):
        """
        Checks if an edge exists within the database with
        the given source and destination nodes.

        :param edge: The edge to query.
        """
        with closing(self.db.cursor()) as cursor:
            cursor.execute(*SQL.select_one(edge.src, edge.rel, edge.dst))
            return bool(tuple(cursor))

    @property
    def find(self):
        """
        Returns a Query object.
        """
        return Query(self.db)
