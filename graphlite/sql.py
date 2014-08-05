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
    smt = 'INSERT INTO %s (src, dst) VALUES (?, ?)'
    return (smt % (rel)), (src, dst)


def remove(src, rel, dst):
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
    return 'SELECT dst FROM %s WHERE src = ?' % (rel), \
           (src,)


def inverse_relation(dst, rel):
    return 'SELECT src FROM %s WHERE dst = ?' % (rel), \
            (dst,)

def select_one(src, rel, dst):
    smt = 'SELECT id FROM %s WHERE src = ? AND dst = ? LIMIT 1'
    return smt % (rel), (src, dst)

