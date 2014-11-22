import MySQLdb

__author__ = 'jesse bostic'
__author__ = 'nick ames'


def open_conn():
    db = MySQLdb.connect(host="50.62.209.116", port=3306, user="TCSS_445", passwd="L3mm31N!", db="Snootboots")
    cur = db.cursor()
    return db, cur


def close_conn(db, cur):
    db.close()
    cur.close()


def connection(query_func):
    """Decorator takes query function and returns result."""

    def doit(table=None):
        db, cur = open_conn()
        if table is None:
            cur.execute(query_func())
        else:
            cur.execute(query_func(table))
        result = cur.fetchall()
        close_conn(db, cur)
        return result

    return doit

@connection
def get_boot_shapes():
    return "SELECT DISTINCT Shape FROM BOOTS"

@connection
def get_tie_lengths():
    return "SELECT DISTINCT Length FROM TIES"

@connection
def get_clasp_types():
    return "SELECT DISTINCT Type FROM CLASPS"

@connection
def get_materials(table):
    table = table.upper() + 'S'
    return "SELECT DISTINCT Material FROM " + table

@connection
def get_colors(table):
    table = table.upper() + 'S'
    return "SELECT DISTINCT Color FROM " + table

@connection
def get_mfgs(table):
    table = table.upper() + 'S'
    return "SELECT DISTINCT MFGS.Name FROM ("+table+" JOIN MFGS ON Mfg = MFGS.ID)"



# EXAMPLE DB CALL W/O DECORATOR
#
# def get_boot_mfgs():
#
#     db, cur = open_conn()
#     cur.execute("SELECT DISTINCT MFGS.Name FROM (BOOTS JOIN MFGS ON Mfg = MFGS.ID)")
#     result = cur.fetchall()
#     close_conn(db, cur)
#     return result



