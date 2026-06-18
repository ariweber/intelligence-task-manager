import logging
import mysql.connector

logger = logging.getLogger(__name__)


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
            logger.info(f"Connected to database {self._db_name}")
        except mysql.connector.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise 

    def get_connection(self):
        if self.conn is None or not self.conn.is_connected():
            logger.info("No active connection, establishing a new one")
            self.connect()
        return self.conn

    def create_database(self):
        conn = mysql.connector.connect(**self._config)
        cursor = conn.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS Intelligence_db""")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Database {self._db_name} is ready")

    def create_tables(self):
        logger.info("Creating tables if they do not exist")
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
                       description TEXT NOT NULL,
                       importance INT NOT NULL,
                       location VARCHAR(50) NOT NULL,
                       difficulty INT NOT NULL,
                       status ENUM('New', 'Assigned', 'In Progress', 'Completed', 'Failed', 'Cancelled') DEFAULT "New",
                       risk_level ENUM('Low', 'Medium', 'High', 'Critical')  NOT NULL,
                       assigned_agent_id INT)""")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Tables are ready")


    def setup(self):
        logger.info("Running database setup")
        self.create_database()
        self.create_tables()
        logger.info("Database setup complete")

DB = DBconnection()
