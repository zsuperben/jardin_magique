__author__ = 'zsb'
import MySQLdb
import MySQLdb.cursors
import logging

logger = logging.getLogger('api')

def get_cursor():
    return get_connection().cursor()


def executeSQL(cursor, statement):
    try:
        return cursor.execute(statement)
    except Exception:
        logger.error('SQL FAILED: ' + statement)
        raise

def get_table_for_zone(con, zone):
    if type(con) is not MySQLdb.connections.Connection or type(zone) is not str:
        raise ValueError('Non biloute c\'est pas une connection')

    mycur =con.cursor(MySQLdb.cursors.DictCursor)
    try:
        if executeSQL(mycur, "DESCRIBE %s" %  zone) > 0:
            logger.debug(mycur.fetchall())
            return True
        else:
            logger.error('No measure table found for %s ' % zone)
            return False
    except MySQLdb.ProgrammingError:
        return False

def set_table_for_zone(con, zone):
    if type(con) is not MySQLdb.connections.Connection or type(zone) is not str:
        raise ValueError('Non biloute')
    mycur =con.cursor(MySQLdb.cursors.DictCursor)


    req = "CREATE TABLE " + zone + """ ( `time` datetime(6) NOT NULL,
    `plant` smallint(5) NOT NULL,
    `soil` int(16) NOT NULL,
    `temp` float(4,2),
    PRIMARY KEY (`time`)  )"""
    logger.debug(req)
    num = executeSQL(mycur, req)
    logger.debug(num)

    con.commit()


def insert_dict_into_db(connection, table, data):
    if type(connection) is not MySQLdb.connections.Connection:
        raise ValueError("First argument has to be a valid mysql connection object")
    if type(data) is not dict:
        raise ValueError("data has to be of type dict")
    if type(table) is not str:
        raise ValueError("table has to be a string")
    mycur = connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        ret = executeSQL(mycur, "DESCRIBE %s ;" % table)
        if ret > 0:
            table_schema = mycur.fetchall()
            list_db = []
            my_values = '('
            for item in table_schema:
                list_db.append(item['Field'])
            for column in  list_db:
                if column not in data.keys():
                    raise ValueError("dict <=> table mismatch")
                else:
                    if type(data[column]) is str:
                        data[column] = '"' +data[column] + '"'
                    my_values = my_values + str(data[column] )+', '
            my_values = my_values[:-2] + ')'
    except MySQLdb.MySQLError:
        raise ValueError("Table must be a valid table.")

    # If all of the above checks are passed then we can pretty much dump the thing on the db
    gogetit = "INSERT INTO "+ table +' VALUES '+ my_values +';'
    logger.debug(gogetit)
    logger.warning('inserting %s into %s' %(data, table))
    logger.warning(gogetit)
    r = executeSQL(mycur, gogetit)
    connection.commit()

def get_last(connection, thing=None, limit=1, *args, **kwargs):
    if type(connection) is not MySQLdb.connections.Connection or ( type(thing) is not str and thing is not "" ):
        raise ValueError("Wrong arguments supplied.")
    mycur = connection.cursor(MySQLdb.cursors.DictCursor)
    if thing is not None and thing not in ["tomates", "seeds","remplissage_cuve", "exterior", "cuve", "mail" ]:
        raise ValueError("type not supported yet")

    if thing is not None:

        if not limit: 
            ret = executeSQL(mycur, "SELECT `time` FROM events WHERE `type`=\"%s\" ORDER BY `time` DESC; " % thing)
        else:
            ret = executeSQL(mycur, "SELECT `time` FROM events WHERE `type`=\"%s\" ORDER BY `time` DESC LIMIT %d ; " % (thing, limit))

    else:
        if not limit:
            ret = executeSQL(mycur, "SELECT * FROM events");
        else:
            ret = executeSQL(mycur, "SELECT * FROM events LIMIT %d" % limit);

    if ret > 0:
        results = mycur.fetchall()
        print(results)
        try:
            for r in results:
                r['time'] = r['time'].isoformat()
            if limit == 1:
                return results[0]
            else:
                return results
        except NameError:
            logger.error("No Time here bob")
            return None
    else:
        return None
def get_cuve(connection, *args, **kwargs):
    mycur = connection.cursor()
    ret = executeSQL(mycur, "SELECT value FROM cuve ORDER BY time DESC LIMIT 1;")
    res =  mycur.fetchone()[0]
    print(res)
    if ret == 1:
        return res
    else:
        return 0

def get_connection():
    return MySQLdb.connect("localhost", "celery", "ffsomg2016", "jardin")

def get_duration(name):
    if type(name) is not str:
        raise ValueError("Get duraiton uses string as an input")
    con = get_connection()
    cur = con.cursor()
    r = executeSQL(cur, "SELECT duration FROM durations WHERE type='%s'" % name)
    if r>0:
        return cur.fetchone()[0]
    else:
        return None


def get_measures():
    cur = get_cursor()
    r = executeSQL(cur,"SHOW TABLES LIKE 'mesure_tbl_%'")
    my_values = []
    if r > 0:
        tables = cur.fetchall()
        #print("Tables contains : %s and is type %s" % (tables, type(tables)))
        for t in tables:
            tmp_list = []
            print(t)
            r = cur.execute("SELECT * FROM %s ORDER BY TIME DESC LIMIT 10 "%t[0] )
            if r > 0:
                tmp = cur.fetchall()
                for v in tmp:
                    tmp_list.append(v)
                my_values.append(tmp_list)

    return my_values

