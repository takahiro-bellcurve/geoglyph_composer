import os, sys

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.oneshot.mysql.mysql_connector import MysqlConnector

def main():
    query = '''
    CREATE TABLE zozotown_goods (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        brand_id VARCHAR(255) NOT NULL,
        goods_id VARCHAR(255) NOT NULL,
        goods_url VARCHAR(255) NOT NULL,
        goods_name VARCHAR(255) NOT NULL,
        gender VARCHAR(255),
        price INT,
        category_id INT,
        child_category_id INT,
        description TEXT,
        material VARCHAR(255),
        created_at DATETIME NOT NULL
    )'''

    db = MysqlConnector()
    db.execute(query)

if __name__ == "__main__":
    main()
