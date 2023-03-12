import os, sys

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.oneshot.mysql.mysql_connector import MysqlConnector

def main():
    query = '''
    CREATE TABLE zozotown_brands (
        id INT NOT NULL AUTO_INCREMENT,
        brand_id VARCHAR(255) NOT NULL,
        brand_url VARCHAR(255) NOT NULL,
        brand_name VARCHAR(255) NOT NULL,
        brand_name_kana VARCHAR(255),
        created_at DATETIME NOT NULL
    )'''

    db = MysqlConnector()
    db.execute(query)

if __name__ == "__main__":
    main()
