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
    """
    Returns the SQL query for selecting the destination
    nodes given a relation and a source node.

    :param src: The source node.
    :param rel: The relation.
    """
    statement = 'SELECT dst FROM %s WHERE src = ?'
    return statement % (rel), (src,)


def inverse_relation(dst, rel):
    """
    Similar to :meth:``forwards_relation`` but selects
    the source nodes instead, given a destination node.

    :param dst: The destination node.
    :param rel: The relation.
    """
    statement = 'SELECT src FROM %s WHERE dst = ?'
    return statement % (rel), (dst,)


def select_one(src, rel, dst):
    """
    Create an SQL query that selects one ID from a
    relation table given a source and destination node.

    :param src: The source node.
    :param rel: The relation.
    :param dst: The destination node.
    """
    smt = 'SELECT id FROM %s WHERE src = ? AND dst = ? LIMIT 1'
    return smt % (rel), (src, dst)


def compound_fwd_query(query, rel):
    """
    Create a compound forwards query that selects the
    destination nodes, which have source nodes within
    the subquery.

    :param query: The subquery.
    :param rel: The relation.
    """
    smt = 'SELECT dst FROM %s WHERE src IN (%s)'
    return smt % (rel, query), tuple()


def compound_inv_query(query, rel, dst):
    """
    Create a compound inverse query, similar to
    :meth:``compound_fw_query`` but only selects
    the source nodes given a destination node.

    :param query: The subquery.
    :param rel: The relation.
    :param dst: The destination node.
    """
    smt = 'SELECT src FROM %s WHERE src IN (%s) AND dst = ?'
    return smt % (rel, query), (dst,)
