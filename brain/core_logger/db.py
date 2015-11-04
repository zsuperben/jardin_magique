__author__ = 'zsb'
import MySQLdb
import MySQLdb.cursors



def get_table_for_zone(con, zone):
    if type(con) is not MySQLdb.connections.Connection or type(zone) is not str:
        raise ValueError('Non biloute')

    mycur =con.cursor(MySQLdb.cursors.DictCursor)
    try:
        if mycur.execute("DESCRIBE %s" %  zone) > 0:
            print(mycur.fetchall())
            return True
        else:
            print('False !!! ')
            return False
    except MySQLdb.ProgrammingError:
        return False

def set_table_for_zone(con, zone):
    if type(con) is not MySQLdb.connections.Connection or type(zone) is not str:
        raise ValueError('Non biloute')
    mycur =con.cursor(MySQLdb.cursors.DictCursor)


    req = "CREATE TABLE " + zone + " ( `time` datetime(6) NOT NULL, `plant` smallint(5) NOT NULL, `soil` int(16) NOT NULL, PRIMARY KEY (`time`)  )"
    print(req)
    num = mycur.execute(req)
    print num

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
        ret = mycur.execute("DESCRIBE %s ;" % table)
        if ret > 0:
            table_schema = mycur.fetchall()
            list_db =[]
            my_values = '('
            for item in table_schema:
                list_db.append(item['Field'])
            for column in  list_db:
                if column not in data.keys():
                    raise ValueError("dict <=> table mismatch")
                else:
                    my_values = my_values + str(data[column] )+',\n'
            my_values = my_values[:-2] + ')'
    except MySQLdb.MySQLError:
        raise ValueError("Table must be a valid table.")

    # If all of the above checks are passed then we can pretty much dump the thing on the db
    gogetit = "INSERT INTO "+ table +' VALUES '+ my_values +';'
    print(gogetit)
    r = mycur.execute(gogetit)
    connection.commit()
