import pymysql
import os

class F1:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = os.environ.get('DBUSER')
        pw = os.environ.get('DBPW')
        host = os.environ.get('DBHOST')

        conn = pymysql.connect(
            user= usr,
            password=pw,
            host= host,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_circuits_name():

        sql = "SELECT name FROM F1.circuits";
        conn = F1._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result

    @staticmethod
    def append_new_circuits_name(id, Ref, name, loc, country, lat, lng, alt, url):
        sql = "INSERT INTO F1.circuits VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        conn = F1._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (id, Ref, name, loc, country, lat, lng, alt, url))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            return e

    @staticmethod
    def delete_circuits(id):
        sql = "DELETE from F1.circuits where circuitId = %s;"
        conn = F1._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (id))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            return e

    @staticmethod
    def update_circuits(name, value):
        sql = "UPDATE F1.circuits set name = %s where circuitId = %s;"
        conn = F1._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (value, name))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            return e



