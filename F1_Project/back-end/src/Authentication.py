import pymysql
import os

class Auth:

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
    def login_check(user, pw):
        sql = "SELECT pw FROM lg.users where user = %s";
        conn = Auth._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, user)
        result = cur.fetchone()
        if result['pw'] == pw:
            return True
        return False
