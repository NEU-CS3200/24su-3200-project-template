import pymysql

_db = None


def get_cursor():
    if not _db:
        raise ValueError("DB is not initialized!")

    return _db.cursor()


def init_db(host, port, user, pwd, db_name):
    global _db
    _db = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=pwd,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def cleanup_db():
    global _db
    _db.close()
    _db = None
