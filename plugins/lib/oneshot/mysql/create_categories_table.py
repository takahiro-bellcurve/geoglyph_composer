import os, sys, json

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.mysql_connector import MysqlConnector

def main():
    query = '''
    CREATE TABLE zozotown_categories (
        id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        path VARCHAR(255) NOT NULL
    )'''

    db = MysqlConnector()
    db.write(query)


    with open('../data/zozotown_category.json') as f:
        data = json.load(f)

    category_dict = data['categorydata']
    categories = list(category_dict.keys())


    values = []
    for category in categories:
        values.append([ category, category_dict[category]['name'], category_dict[category]['path']])

    insert_data(values)


def insert_data(values):
    query = '''
    INSERT INTO zozotown_categories (id, name, path) VALUES (%s, %s, %s)
    '''

    db = MysqlConnector()
    db.write_many(query, values)

if __name__ == "__main__":
    main()
