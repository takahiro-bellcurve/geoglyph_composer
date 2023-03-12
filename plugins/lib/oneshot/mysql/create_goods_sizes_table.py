import os, sys

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.oneshot.mysql.mysql_connector import MysqlConnector

def main():
    query = '''
    CREATE TABLE zozotown_good_sizes (
        id INT NOT NULL AUTO_INCREMENT,
        goods_id VARCHAR(255) NOT NULL,
        size VARCHAR(255) NOT NULL,
        info JSON NOT NULL, 
    )'''

    db = MysqlConnector()
    db.execute(query)

if __name__ == "__main__":
    main()
