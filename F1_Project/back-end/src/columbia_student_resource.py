import pymysql
import os


class ColumbiaStudentResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = os.environ.get('DBUSER')
        pw = os.environ.get('DBPW')
        host = os.environ.get('DBHOST')

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host= host,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):

        sql = "SELECT * FROM f22_databases.columbia_student where uni=%s";
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result
    @staticmethod
    def get_by_firstname(info):
        sql = "SELECT * FROM f22_database.sample_student_info where first_name=%s";
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, info)
        result = cur.fetchall()
        return result
    @staticmethod
    def get_address_by_first_name(info):
        sql = "SELECT email FROM f22_database.sample_student_info where first_name=%s";
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, info)
        result = cur.fetchall()
        return result
    @staticmethod
    def get_info_by_firstname_address(firstname, address):
        sql = "SELECT * FROM f22_database.sample_student_info where first_name=%s and email=%s";
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (firstname, address))
        result = cur.fetchall()
        return result
    @staticmethod
    def get_info_by_firstname_lastname(firstname, lastname):
        sql = "SELECT * FROM f22_database.sample_student_info where first_name=%s and last_name=%s";
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (firstname, lastname))
        result = cur.fetchall()
        return result
    @staticmethod
    def append_new_students(student_id, first_name, middle_name, last_name, email, school_code):
        sql = "INSERT INTO f22_database.sample_student_info VALUES (%s, %s, %s, %s, %s, %s);"
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (student_id, first_name, middle_name, last_name, email, school_code))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            return e

    @staticmethod
    def update_students_by_firstname(first_name, email):
        sql = "UPDATE f22_database.sample_student_info set email = %s where first_name = %s;"
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, (email, first_name))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            return e

    @staticmethod
    def delete_students_by_firstname(first_name):
        sql = "DELETE from f22_database.sample_student_info where first_name=%s;"
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        try:
            conn.begin()
            res = cur.execute(sql, first_name)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            return e