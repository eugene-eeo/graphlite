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
    """

    def __init__(self, db):
        self.db = db
        self.ops = []

    def store_many(self, edges):
        """
        Store many edges into the database. Similar to the
        :meth:`graphlite.transaction.Transaction.delete_many`
        method.

        :param edges: An iterable of edges to store.
        """
        self.ops.append((SQL.store, edges))

    def delete_many(self, edges):
        """
        Delete multiple edge queries from the database. Best
        used when you have a fairly large generator that
        shouldn't be loaded into memory at once for efficiency
        reasons.

        :param edges: An iterable of edges or ``Graph.find``
            style edge queries to delete.
        """
        self.ops.append((SQL.remove, edges))

    def store(self, edge):
        """
        Store an edge in the database. Both the source
        and destination nodes must be specified, as
        well as the relation.

        :param edge: The edge.
        """
        self.store_many((edge,))

    def delete(self, edge):
        """
        Deletes an edge from the database. Either the
        source node or destination node `may` be specified,
        but the relation has to be specified.

        :param edge: The edge.
        """
        self.delete_many((edge,))

    def abort(self):
        """
        Raises an ``AbortSignal``. If you used the
        ``Graph.transaction`` context manager this
        exception is automatically caught and ignored.
        """
        self.clear()
        raise AbortSignal

    def _perform_ops(self, cursor):
        for operation, edges in self.ops:
            for edge in edges:
                cursor.execute(*operation(
                    src=edge.src,
                    rel=edge.rel,
                    dst=edge.dst,
                ))

    def perform_ops(self):
        """
        Performs the stored operations on the database
        connection.
        """
        with self.db:
            with closing(self.db.cursor()) as cursor:
                cursor.execute('BEGIN TRANSACTION')
                self._perform_ops(cursor)

    def clear(self):
        """
        Clears all the operations registered on the
        transaction object.
        """
        del self.ops[:]

    def commit(self):
        """
        Commits the stored changes to the database.
        You `don't` have to call this function if
        the transaction object is used as a context
        manager. A transaction can only be committed
        once.
        """
        try:
            self.perform_ops()
        finally:
            self.clear()

    def __enter__(self):
        """
        Enter a transaction, and returns the current
        transaction object to the caller for
        convenience.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Commits the transaction if no tracebacks or
        exceptions were raised and if operations were
        defined. Ignores ``AbortSignal``.
        """
        if not traceback and self.ops:
            self.commit()
        return isinstance(value, AbortSignal)
