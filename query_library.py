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

def action(name, comp_list):
    """Finds what button was pressed and queries based on boot, tie or clasp"""

    def valid_price(p):
        """Tests if a price is a valid number"""
        try:
            float(p)
            return True
        except ValueError:
            return False

    query = "SELECT * FROM (" + name.upper() + "S" + " JOIN MFGS ON Mfg = MFGS.ID)"
    # Name entry
    text = comp_list[0].get()
    if text == "Name" or text == "":
        text = ""
    else:
        # Two cases, names containing text OR names == text
        text = name.upper() + "S.Name LIKE " + "'%" + text + "%'"
        #text = name.upper() + "S.Name=" + "'" + text + "'"

    # Dropdown values
    drop1 = comp_list[1].cget("text")
    if drop1 != "Shape" and drop1 != "ALL" and name == "Boot":
        drop1 = "Shape=" + "'" + drop1 + "'"
    elif drop1 != "Length" and drop1 != "ALL" and name == "Tie":
        drop1 = "Length=" + "'" + drop1 + "'"
    elif drop1 != "Type" and drop1 != "ALL" and name == "Clasp":
        drop1 = "Type=" + "'" + drop1 + "'"
    else:
        drop1 = ""

    drop2 = comp_list[2].cget("text")
    if drop2 != "Material" and drop2 != "ALL":
        drop2 = "Material=" + "'" + drop2 + "'"
    else:
        drop2 = ""

    drop3 = comp_list[3].cget("text")
    if drop3 != "Color" and drop3 != "ALL":
        drop3 = "Color=" + "'" + drop3 + "'"
    else:
        drop3 = ""

    drop4 = comp_list[4].cget("text")
    if drop4 != "Manufacturer" and drop4 != "ALL":
        drop4 = "MFGS.Name=" + "'" + drop4 + "'"
    else:
        drop4 = ""

    # prices
    min = comp_list[5].get()
    max = comp_list[6].get()

    if min == "Min Price" or min == "":
        min = ""
    else:
        if valid_price(min):
            min = "Price>" + min
        else:
            min = "Invalid input for min price."

    if max == "Max Price" or max == "":
        max = ""
    else:
        if valid_price(max):
            max = "Price<" + max
        else:
            max = "Invalid input for max price."

    # build the query statement, check for no/bad inputs
    if text != "" or drop1 != "" or drop2 != "" or drop3 != "" or drop4 != "" or min != "" or max != "":
        query += " WHERE "
    else:
        #query db here for ANY
        print(query)
        res = find(query)
        print(res)
        return

    # build the statement
    andit = False
    if text != "":
        query += text + " "
        andit = True
    if drop1 != "":
        if andit:
            query += "AND "
        query += drop1 + " "
        andit = True
    if drop2 != "":
        if andit:
            query += "AND "
        query += drop2 + " "
        andit = True
    if drop3 != "":
        if andit:
            query += "AND "
        query += drop3 + " "
        andit = True
    if drop4 != "":
        if andit:
            query += "AND "
        query += drop4 + " "
        andit = True
    if min != "":
        if min != "Invalid input for min price.":
            if andit:
                query += "AND "
            query += min + " "
            andit = True
        else:
            # error here don't query
            print(min)
            return
    if max != "":
        if max != "Invalid input for max price.":
            if andit:
                query += "AND "
            query += max + " "
        else:
            # error here don't query
            print(max)
            return
    print(query)
    res = find(query)
    print(res)
    return

@connection
def find(statement):
    return statement

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



