import pymysql
import datetime
import jwt

class User():
    def __init__(self):
        pass

    @staticmethod
    def encode_auth_token(user_id, secret_key):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                # app.config.get('SECRET_KEY'),
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def update_authtoken(user_id, token):
        sql = "UPDATE user_profile.user_info SET auth_token = %s WHERE (user_id = %s);"
        data = (token, user_id)
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit() 

    @staticmethod
    def checkUser(user_id):
        sql = "select user_id,email,name,profile_pic from user_profile.user_info where user_id = %s;"
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=user_id)
        result = cur.fetchone()
        if result == None:
            return None

        return True

    @staticmethod
    def checkAuthToken(user_id, token):
        sql = "select * from user_profile.user_info where user_id = %s and auth_token = %s;"
        conn = User._get_connection()
        data = (user_id, token)
        cur = conn.cursor()
        res = cur.execute(sql, data)
        result = cur.fetchone()
        if result == None:
            return False
        return True
    
    @staticmethod
    def logout(user_id):
        sql = "UPDATE user_profile.user_info SET auth_token = '1' WHERE (user_id = %s);"
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=user_id)
        conn.commit()

    @staticmethod
    def create(id_, name, email, profile_pic, token):
        sql = "insert into user_profile.user_info(user_id, email, name, profile_pic, auth_token) values (%s, %s, %s, %s, %s)"
        data = (id_, email, name, profile_pic, token)
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit() 

    @staticmethod
    def _get_connection():

        # usr = os.environ.get("DBUSER")
        # pw = os.environ.get("DBPW")
        # h = os.environ.get("DBHOST")
        usr = "xxxx"
        pw = "xxxx"
        h = "xxxx"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_userid_by_email(email):
        sql = "select user_id from user_profile.user_info where email = %s";
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=email)
        result = cur.fetchone()
        if result == None:
            return -1
        return result['user_id']


    @staticmethod
    def get_user_allergy_by_id(user_id):
        sql = "SELECT allergy FROM user_profile.user_allergy where user_id = %s";
        conn = User._get_connection()
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
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit() 

    @staticmethod
    def add_allergy_by_user_id(user_id, allergy):
        sql = "insert into user_profile.user_allergy(user_id, allergy) values (%s, %s)"
        data = (user_id, allergy)
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit()

    @staticmethod
    def delete_allergy_by_user_id(user_id, allergy):
        sql = "delete from user_profile.user_allergy where user_id = %s and allergy = %s"
        data = (user_id, allergy)
        conn = User._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, data)
        conn.commit()
