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
        self.ops.append((SQL.store, edge))

    def delete(self, edge):
        """
        Deletes an edge from the database. Either the
        source node or destination node `may` be specified,
        but the relation has to be specified.

        :param edge: The edge.
        """
        self.ops.append((SQL.remove, edge))

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
        for operation, edge in self.ops:
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
            try:
                cursor = self.db.cursor()
                with closing(cursor):
                    self.perform_ops(cursor)
                self.db.commit()
            except:
                self.db.rollback()
                raise
