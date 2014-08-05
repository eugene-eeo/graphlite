CREATE_TABLE = '''\
CREATE TABLE IF NOT EXISTS %s
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src UNSIGNED INTEGER,
    dst UNSIGNED INTEGER
)
'''

INDEXES = (
    'CREATE INDEX IF NOT EXISTS src_index ON %s ( src );',
    'CREATE INDEX IF NOT EXISTS dst_index ON %s ( dst );'
)


def store(src, rel, dst):
    """
    Returns an SQL statement to store an edge into
    the SQL backing store.

    :param src: The source node.
    :param rel: The relation.
    :param dst: The destination node.
    """
    smt = 'INSERT INTO %s (src, dst) VALUES (?, ?)'
    return (smt % (rel)), (src, dst)


def remove(src, rel, dst):
    """
    Returns an SQL statement that removes edges from
    the SQL backing store. Either `src` or `dst` may
    be specified, even both.

    :param src: The source node.
    :param rel: The relation.
    :param dst: The destination node.
    """
    smt = 'DELETE FROM %s' % (rel)
    queries = []
    params = []

    for query, item in (('src', src), ('dst', dst)):
        if item is not None:
            queries.append('%s = ?' % (query))
            params.append(item)

    if not queries:
        return smt, params
    smt = '%s WHERE %s' % (smt, ' AND '.join(queries))
    return smt, params


def forwards_relation(src, rel):
    statement = 'SELECT dst FROM %s WHERE src = ?'
    return statement % (rel), (src,)


def inverse_relation(dst, rel):
    statement = 'SELECT src FROM %s WHERE dst = ?'
    return statement % (rel), (dst,)


def select_one(src, rel, dst):
    smt = 'SELECT id FROM %s WHERE src = ? AND dst = ? LIMIT 1'
    return smt % (rel), (src, dst)


def compound_fw_query(rel, query):
    smt = 'SELECT dst FROM %s WHERE src IN (%s)'
    return smt % (rel, query), tuple()


def compound_iv_query(dst, rel, query):
    smt = 'SELECT src FROM %s WHERE src IN (%s) AND dst = ?'
    return smt % (rel, query), (dst,)
