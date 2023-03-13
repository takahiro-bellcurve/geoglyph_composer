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
        check_goods_id = item['goods_id']
        find_query = f"SELECT * FROM `zozotown_goods` WHERE `goods_id` = %s"
        is_exist = self.cur.execute(find_query, check_goods_id)

        if is_exist == 0:
            self._insert_goods(item)
            self._insert_goods_sizes(item)
            self._insert_goods_colors(item)
            self._insert_goods_images(item)
            self.conn.commit()
        else:
            pass
        return item
    
    def _insert_goods(self, item):
        insert_query = """
        INSERT INTO `zozotown_goods` (`brand_id`, `goods_id`, `goods_url`, `goods_name`, `gender`, `price`, `description`, `category_id`, `child_category_id`, `material`, `created_at`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        category_id = self._convert_to_category_id(item['category_path'])
        child_category_id = self._convert_to_child_category_id(item['child_category_path'])
        self.cur.execute(insert_query, (
            item['brand_id'],
            item['goods_id'],
            item['goods_url'],
            item['goods_name'],
            item['gender'],
            item['price'],
            item['description'],
            category_id,
            child_category_id,
            item['material'],
            item['created_at']
        ))

    def _insert_goods_sizes(self, item):
        insert_query = """
        INSERT INTO `zozotown_goods_sizes` (`goods_id`, `size`, `info`)
        VALUES (%s, %s, %s)
        """
        for size in item['sizes']:
            self.cur.execute(insert_query, (
                item['goods_id'],
                size['size'],
                size['info'],
            ))

    def _insert_goods_colors(self, item):
        insert_query = """
        INSERT INTO `zozotown_goods_colors` (`goods_id`, `color`)
        VALUES (%s, %s)
        """
        for color in item['colors']:
            self.cur.execute(insert_query, (
                item['goods_id'],
                color['color'],
            ))

    def _insert_goods_images(self, item):
        insert_query = """
        INSERT INTO `zozotown_goods_images` (`goods_id`, `image_url`)
        VALUES (%s, %s)
        """
        for image in item['images']:
            self.cur.execute(insert_query, (
                item['goods_id'],
                image['image_url'],
            ))
    
    def _convert_to_category_id(self, category_path):
        find_query = f"SELECT id FROM `zozotown_categories` WHERE `path` = %s"
        self.cur.execute(find_query, category_path)
        category_id = self.cur.fetchone()
        return category_id
    
    def _convert_to_child_category_id(self, child_category_path):
        find_query = f"SELECT id FROM `zozotown_child_categories` WHERE `path` = %s"
        self.cur.execute(find_query, child_category_path)
        child_category_id = self.cur.fetchone()
        return child_category_id
        
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
    

