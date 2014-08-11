from contextlib import closing
import graphlite.sql as SQL


class AbortSignal(Exception):
    """
    Signals that the transaction has been aborted.
    """
    pass


class Transaction(object):
    """
    Represents a single, atomic transaction. All
    calls are delayed jobs- they do not execute
    until the transaction is committed.

    :param db: An SQLite connection.
    :param lock: A threading.RLock instance.
    """

    def __init__(self, db, lock):
        self.db = db
        self.lock = lock
        self.ops = []

    def store(self, edge):
        """
        Store an edge in the database. Both the source
        and destination nodes must be specified, as
        well as the relation.

        :param edge: The edge.
        """
        self.store_many((edge,))

    def store_many(self, edges):
        """
        Store many edges into the database. Similar to the
        :meth:`graphlite.transaction.Transaction.delete_many`
        method.

        :param edges: An iterable of edges to store.
        """
        self.ops.append((SQL.store, edges))

    def delete(self, edge):
        """
        Deletes an edge from the database. Either the
        source node or destination node `may` be specified,
        but the relation has to be specified.

        :param edge: The edge.
        """
        self.delete_many((edge,))

    def delete_many(self, edges):
        """
        Delete multiple edge queries from the database. Best
        used when you have a fairly large generator that
        shouldn't be loaded into memory at once for efficiency
        reasons.

        :param edges: An iterable of edge queries to delete.
        """
        self.ops.append((SQL.remove, edges))

    def abort(self):
        """
        Raises an ``AbortSignal``. If you used the
        ``Graph.transaction`` context manager this
        exception is automatically caught and ignored.
        """
        raise AbortSignal

    @property
    def defined(self):
        """
        Returns true if there are any internal
        operations waiting to be performed when the
        commit method is called.
        """
        return bool(self.ops)

    def perform_ops(self, cursor):
        """
        Performs the stored operations on the given
        cursor object.

        :param cursor: The SQLite.Cursor object.
        """
        cursor.execute('BEGIN')
        for operation, edges in self.ops:
            for edge in edges:
                cursor.execute(*operation(
                    src=edge.src,
                    rel=edge.rel,
                    dst=edge.dst,
                ))

    def commit(self):
        """
        Commits the stored changes to the database.
        Note that you `do not` have to call this
        function if you used the ``Graph.transaction``
        context manager, or the transaction will be
        committed twice.
        """
        with self.lock:
            with self.db:
                with closing(self.db.cursor()) as cursor:
                    self.perform_ops(cursor)
