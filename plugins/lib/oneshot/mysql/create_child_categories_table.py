import os, sys, json

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.oneshot.mysql.mysql_connector import MysqlConnector

def main():
    query = '''
    CREATE TABLE child_categories (
        id INT NOT NULL,
        category_id INT NOT NULL
        name VARCHAR(255) NOT NULL,
        path VARCHAR(255) NOT NULL,
    )'''

    db = MysqlConnector()
    db.execute(query)


    with open('../data/zozotown_category.json') as f:
        data = json.load(f)

    category_dict = data['categorydata']
    categories = list(category_dict.keys())


    values = []
    for category in categories:
        for child_category in category_dict[category]["type"]:
            values.append([ child_category["id"], category, child_category["name"], child_category["path"]])

    insert_data(values)


def insert_data(values):
    query = '''
    INSERT INTO categories (id, category_id , name, path) VALUES (%s, %s, %s, %s)
    '''

    db = MysqlConnector()
    db.execute_many(query, values)

if __name__ == "__main__":
    main()
