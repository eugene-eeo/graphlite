from contextlib import closing
from sqlite3 import Connection
from threading import Lock

from graphlite.query import Query
from graphlite.transaction import Transaction
import graphlite.sql as SQL


class Graph(object):
    """
    Initializes a new Graph object.

    :param uri: The URI of the SQLite db.
    :param graphs: Graphs to create.
    """
    def __init__(self, uri, graphs=()):
        self.uri = uri
        self.db = Connection(
            database=uri,
            check_same_thread=False,
            isolation_level=None,
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
            for table in graphs:
                cursor.execute(SQL.CREATE_TABLE % (table))
                for index in SQL.INDEXES:
                    cursor.execute(index % (table))
            self.db.commit()

    def close(self):
        """
        Close the SQLite connection.
        """
        self.db.close()

    __del__ = close

    def __contains__(self, edge):
        """
        Checks if an edge exists within the database
        with the given source and destination nodes.

        :param edge: The edge to query.
        """
        with closing(self.db.cursor()) as cursor:
            cursor.execute(*SQL.select_one(edge.src, edge.rel, edge.dst))
            return cursor.fetchone() is not None

    @property
    def find(self):
        """
        Returns a Query object that acts on the graph.
        """
        return Query(self.db)

    def transaction(self):
        """
        Returns a Transaction object. All modifying
        operations, i.e. ``store``, ``delete`` must
        then be performed on the transaction object.
        """
        return Transaction(self.db, self.lock)
