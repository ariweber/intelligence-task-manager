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
            self.conn = mysql.connector.connect(database=self._db_name, **self._config)
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                       id INT PRIMARY KEY AUTO_INCREMENT,
                       name VARCHAR(50) NOT NULL,
                       specialty VARCHAR(50) NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE,
                       completed_missions INT DEFAULT 0,
                       failed_missions INT DEFAULT 0,
                       agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS missions (
                       id INT PRIMARY KEY AUTO_INCREMENT,
                       title VARCHAR(50) NOT NULL,
                       description TEXT (50) NOT NULL,
                       location VARCHAR(50) NOT NULL,
                       difficulty INT NOT NULL,
                       status ENUM('New', 'Assigned', 'In Progress', 'Completed', 'Failed', 'Cancelled') DEFAULT "New",
                       risk_level ENUM('Low', 'Medium', 'High')  NOT NULL,
                       assigned_agent_id INT)""")
        conn.commit()
        cursor.close()
        conn.close()
    
    
    def setup(self):
        self.create_database()
        self.create_tables()

DB = DBconnection()
