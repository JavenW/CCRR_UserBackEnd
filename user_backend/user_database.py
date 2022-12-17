import pymysql
import os


class UserResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_users():
        sql = "SELECT * FROM user_profile.user_info";
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_user_by_email(email):
        sql = "SELECT allergy FROM user_profile.user_info where email = %s";
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=email)
        result = cur.fetchall()
        return result

    @staticmethod
    def add_user_by_info(email, name, allergy):
        sql = "insert into user_profile.user_info(email, name, allergy) values (%s, %s, %s)"
        data = (email, name, allergy)
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit()

    def delete_user_by_email(email):
        sql = "delete from user_profile.user_info where email = %s"
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, email)
        conn.commit()

    def delete_allergy_by_email_and_allergy(email, allergy):
        sql = "delete from user_profile.user_info where email = %s and allergy = %s"
        data = (email, allergy)
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit()

    def update_phone_by_email_and_phone(email, phone):
        sql = "update user_profile.user_info set phone = %s where email = %s;"
        data = (phone, email)
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit()




