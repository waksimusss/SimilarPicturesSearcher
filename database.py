import psycopg2
from functions import HOG
from PIL.Image import Image
import io
import base64

class DataBase:

    host = "127.0.0.1"
    user = "postgres"
    password = "qwerty"
    db_name = "application"

    def create_connection(self):
        connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
        cursor = connection.cursor()
        return connection, cursor

    def download_pictures(self, text, images):
        try:
            connection, cursor = self.create_connection()
            try:
                for image in images:
                    img = psycopg2.Binary(image)
                    sql = "INSERT INTO pictures (picture_id, request, image) VALUES( ?, ?, ?)"
                    cursor.execute(sql, (text, img))
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while inserting data in cartoon table", error)
            finally:
                connection.commit()
                connection.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)


    def save_image(self, text, image):
        try:
            connection, cursor = self.create_connection()
            try:
                img = psycopg2.Binary(image)
                sql = "INSERT INTO pictures (request, image) VALUES( %s, %s)"
                cursor.execute(sql, (text, img))
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while inserting data in cartoon table", error)
            finally:
                connection.commit()
                connection.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)


    def check_user(self, username, password):
        try:
            connection, cursor = self.create_connection()
            try:
                sql = "SELECT EXISTS (SELECT * FROM users WHERE login = %s AND password = %s);"
                cursor.execute(sql, (username, password,))
                connection.commit()
                return cursor.fetchone()[0]
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while inserting data in users table", error)
            finally:
                connection.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)

    def save_user(self, username, password):
        try:
            connection, cursor = self.create_connection()
            try:
                sql = "INSERT INTO users (login, password) VALUES(%s, %s);"
                cursor.execute(sql, (username, password,))
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while inserting data in cartoon table", error)
            finally:
                connection.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)

    def get_images(self, text):
        try:
            connection, cursor = self.create_connection()
            try:
                sql = "SELECT picture_id, image FROM pictures WHERE request = %s;"
                cursor.execute(sql, (text,))
                return list(cursor.fetchall())
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while inserting data in cartoon table", error)
            finally:
                connection.commit()
                connection.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)


    def check_pictures(self, text):
        try:
            connection, cursor = self.create_connection()
            try:
                sql = "SELECT EXISTS (SELECT * FROM pictures WHERE request = %s);"
                cursor.execute(sql, (text,))
                return cursor.fetchone()[0]
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while searching in Database", error)
            finally:
                connection.commit()
                connection.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)

    def get_image_by_id(self, id):
        try:
            connection, cursor = self.create_connection()
            try:
                sql = "SELECT image FROM pictures WHERE picture_id = %s;"
                cursor.execute(sql, (id,))
                return cursor.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while inserting data in cartoon table", error)
            finally:
                connection.commit()
                connection.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to Database", error)




