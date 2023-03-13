import os, sys, logging
from dotenv import load_dotenv

import pymysql

load_dotenv(f"{os.getenv('BASE_DIR')}/.env")
logger = logging.getLogger(__name__)


class MysqlConnector:
    def __init__(self):
        self.host = os.getenv("MYSQL_DB_HOST")
        self.user = os.getenv("MYSQL_DB_USER")
        self.password = os.getenv("MYSQL_ROOT_PASSWORD")
        self.db = os.getenv("MYSQL_DATABASE")
        self.charset = "utf8mb4"
        self.cusrorType = pymysql.cursors.DictCursor

        logger.info(f"""
          ----- Connection information -----
          host: {self.host}
          user: {self.user}
          password: ******{self.password[-4:]}
          db: {self.db}
          charset: {self.charset}
          ---------------------------------        
          """)
        
        try:
          self.connection = pymysql.connect(
              host=self.host,
              user=self.user,
              password=self.password,
              db=self.db,
              charset=self.charset,
              cursorclass=self.cusrorType
          )
          logger.info("Connection established.")
        except Exception as e:
          logger.error(f"Error Occurred: {e}")
          sys.exit()

    
    def write(self, query, params=None):
        logger.info(f"Executing query: {query}")
        cursor = self.connection.cursor()
        try:
          cursor.execute(query, params)
          self.connection.commit()
          logger.info(f"Query executed successfully.")
        except Exception as e:
          logger.error(f"Error Occurred: {e}")
          self.connection.rollback()
          sys.exit()
        finally:
          cursor.close()
          logger.info("Cursor closed.")

    def write_many(self, query, params=None):
        logger.info(f"Executing query: {query}")
        cursor = self.connection.cursor()
        try:
          cursor.executemany(query, params)
          self.connection.commit()
          logger.info(f"Query executed successfully.")
        except Exception as e:
          logger.error(f"Error Occurred: {e}")
          self.connection.rollback()
          sys.exit()
        finally:
          cursor.close()
          logger.info("Cursor closed.")
    
    def read(self, query, params=None):
        logger.info(f"Executing query: {query}")
        cursor = self.connection.cursor()
        try:
          cursor.execute(query, params)
          res = cursor.fetchall()
          logger.info(f"Query executed successfully.")
        except Exception as e:
          logger.error(f"Error Occurred: {e}")
          self.connection.rollback()
          sys.exit()
        finally:
          cursor.close()
          logger.info("Cursor closed.")
        return res
