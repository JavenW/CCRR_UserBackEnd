import pymysql
import os


class UserResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        # usr = os.environ.get("DBUSER")
        # pw = os.environ.get("DBPW")
        # h = os.environ.get("DBHOST")
        usr = "admin"
        pw = "dbuserdbuser"
        h = "userdb.ci9bmsfj6m9q.us-east-1.rds.amazonaws.com"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    # @staticmethod
    # def get_users():
    #     sql = "SELECT * FROM user_profile.user_info";
    #     conn = UserResource._get_connection()
    #     cur = conn.cursor()
    #     res = cur.execute(sql)
    #     result = cur.fetchall()
    #     return result

    @staticmethod
    def get_userid_by_email(email):
        sql = "select user_id from user_profile.user_info where email = %s";
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=email)
        result = cur.fetchone()
        if result == None:
            return -1
        return result['user_id']


    @staticmethod
    def get_user_allergy_by_email(email):
        user_id = UserResource.get_userid_by_email(email)
        sql = "SELECT allergy FROM user_profile.user_allergy where user_id = %s";
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=user_id)
        result = cur.fetchall()
        allergies = []
        for pair in result:
            allergies.append(pair['allergy'])
        return allergies

    @staticmethod
    def add_user_by_info(email, name):
        sql = "insert into user_profile.user_info(email, name) values (%s, %s)"
        data = (email, name)
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit() 

    @staticmethod
    def add_allergy_by_email(email, allergy):
        user_id = UserResource.get_userid_by_email(email)
        sql = "insert into user_profile.user_allergy(user_id, allergy) values (%s, %s)"
        data = (user_id, allergy)
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit()

    @staticmethod
    def delete_allergy_by_email(email, allergy):
        user_id = UserResource.get_userid_by_email(email)
        sql = "delete from user_profile.user_allergy where user_id = %s and allergy = %s"
        data = (user_id, allergy)
        conn = UserResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit()

a = UserResource
print(a.get_userid_by_email("jw4156@columbia.e2du"))


