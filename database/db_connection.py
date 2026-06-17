import mysql.connector

class DBconnection:
    def __init__(self):
        self.conn = None
        self._config ={
            "host": "localhost",
            "user": "root",
            "password": "1234",
            "port": 3306}
        self._db_name = "Intelligence_db"

    def connect(self):
        try:
            self.conn = mysql.connector.connect(self._db_name, **self._config)
        except mysql.connector.Error as e:
            raise    

    def get_connection(self):
        if self.conn == None or self.conn.is_connected:
            self.connect()
        return self.conn

    def create_database(self):
        conn = mysql.connector.connect(**self._config)
        cursor = conn.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS Intelligence_db""")
        conn.commit()
        cursor.close()
        conn.close()

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE agents(
                       id INT PRIMARY KEY AUTO_INCREMENT,
                       

                       ) """)
