from contextlib import closing
import graphlite.sql as SQL


class AbortSignal(Exception):
    pass


class Transaction(object):
    def __init__(self, db, lock):
        self.db = db
        self.lock = lock
        self.ops = []

    def store(self, edge):
        self.ops.append((SQL.store, edge))

    def delete(self, edge):
        self.ops.append((SQL.remove, edge))

    def abort(self):
        raise AbortSignal

    @property
    def defined(self):
        return bool(self.ops)

    def perform_ops(self, cursor):
        for operation, edge in self.ops:
            cursor.execute(*operation(
                src=edge.src,
                rel=edge.rel,
                dst=edge.dst,
            ))

    def commit(self):
        with self.lock:
            try:
                cursor = self.db.cursor()
                cursor.execute('BEGIN')
                with closing(cursor):
                    self.perform_ops(cursor)
                self.db.commit()
            except:
                self.db.rollback()
                raise
