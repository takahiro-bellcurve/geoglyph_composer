import os, sys

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.mysql_connector import MysqlConnector

def main():
    query = '''
    CREATE TABLE zozotown_goods_images (
        id INT NOT NULL AUTO_INCREMENT  PRIMARY KEY,
        goods_id VARCHAR(255) NOT NULL,
        image_url VARCHAR(255) NOT NULL
    )'''

    db = MysqlConnector()
    db.write(query)

if __name__ == "__main__":
    main()
