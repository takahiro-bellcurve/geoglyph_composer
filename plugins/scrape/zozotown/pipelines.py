import os, sys
from dotenv import load_dotenv

from itemadapter import ItemAdapter
import pymysql

sys.path.append(os.getenv("BASE_DIR"))
load_dotenv(".env")


class MysqlPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=os.getenv("MYSQL_DB_HOST"),
            user=os.getenv("MYSQL_DB_USER"),
            password=os.getenv("MYSQL_ROOT_PASSWORD"),
            db=os.getenv("MYSQL_DATABASE"),
            charset="utf8mb4"
        )
        self.cur = self.conn.cursor()


class ZozotownBrandsPipeline(MysqlPipeline):    
    def process_item(self, item, spider):
        check_brand_id = item['brand_id']
        find_query = f"SELECT * FROM `zozotown_brands` WHERE `brand_id` = %s"
        is_exist = self.cur.execute(find_query, check_brand_id)

        if is_exist == 0:
            insert_query = """
            INSERT INTO `zozotown_brands` (`brand_id`, `brand_url`, `brand_name`, `brand_name_kana`, `created_at`)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cur.execute(insert_query, (
                item['brand_id'],
                item['brand_url'],
                item['brand_name'],
                item['brand_name_kana'],
                item['created_at']
            ))
            self.conn.commit()
        else:
            pass
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

class ZozotownBrandGoodsPipeline(MysqlPipeline):
    def process_item(self, item, spider):
        check_brand_id = item['brand_id']
        find_query = f"SELECT * FROM brands WHERE brand_id = '{check_brand_id}'"
        is_exist = self.cur.execute(find_query, check_brand_id)

        if is_exist:
            insert_query = f"""
            INSERT INTO brand_goods (brand_id, goods_id, goods_url, goods_name, goods_name_kana, created_at)
            VALUES ({item['brand_id']}, {item['goods_id']}, {item['goods_url']}, {item['goods_name']}, {item['goods_name_kana']}, {item['created_at']})
            """
            self.cur.execute(insert_query, (
                item['brand_id'],
                item['goods_id'],
                item['goods_url'],
                item['goods_name'],
                item['goods_name_kana'],
                item['created_at']
            ))
            self.conn.commit()
        else:
            pass
        return item
    
    def close_spider(self):
        self.cur.close()
        self.conn.close()



