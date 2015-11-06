__author__ = 'zsb'

import MySQLdb as mdb
import MySQLdb.cursors


class decision_maker(object):
    def __init__(self, conf):
        try:
            self.dbc = mdb.connect(conf['db']['host'],
                                   conf['db']['user'],
                                   conf['db']['pass'],
                                   conf['db']['db'])
            cur = self.dbc.cursor()
            self.cur = cur
            self.dcur = self.dbc.cursor(MySQLdb.cursors.DictCursor)
            if self.cur.execute('SHOW TABLES LIKE "mesure_tbl_%";') > 0:
                rset_tbl = self.cur.fetchall()[0]
                self.mesure_tables = []
                for t in rset_tbl:
                    self.mesure_tables.append(t)

            # We need to also get more info about the plants per zone
            self.topos = {}
            for mtbl in self.mesure_tables:
                self.topos[mtbl] = {}
                if self.dcur.execute("SELECT `plant` FROM `%s` ;" % mtbl ) > 0:
                    p = self.dcur.fetchone()['plant']
                    while p:
                        try:
                            if p not in self.topos[mtbl]:
                                self.topos[mtbl][p] = None
                                if self.dcur.execute("SELECT `espece_id` FROM `core_plant` WHERE `position`=" + str(p) +";") > 0:
                                    espece_id = self.dcur.fetchone()['espece_id']
                                    if self.dcur.execute("select * from `core_planttype` WHERE `id`=" + str(espece_id) + ";" ) > 0:
                                        self.topos[mtbl][p]= self.dcur.fetchone()
                            p = self.dcur.fetchone()['plant']
                        except TypeError:
                            break

        except NameError as e:
            print("Config file incomplete!")
            raise e


if __name__ == '__main__':
    d = {
        'db': {
            'host': '192.168.0.2',
            'password': 'biloute',
            'db': 'jardin',
            'user': 'test_laptop',
            'pass': 'biloute'}
    }

    m = decision_maker(d)