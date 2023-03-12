# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class BrandItem(scrapy.Item):
    brand_id = scrapy.Field(output_processor=TakeFirst())
    brand_name = scrapy.Field(output_processor=TakeFirst())
    brand_name_kana = scrapy.Field(output_processor=TakeFirst())
    brand_url = scrapy.Field(output_processor=TakeFirst())
    created_at = scrapy.Field(output_processor=TakeFirst())



class GoodsSizeItem(scrapy.Item):
    goods_id = scrapy.Field(output_processor=TakeFirst())
    size = scrapy.Field(output_processor=TakeFirst())
    info = scrapy.Field(output_processor=TakeFirst())
    created_at = scrapy.Field(output_processor=TakeFirst())

class GoodsColorItem(scrapy.Item):
    goods_id = scrapy.Field(output_processor=TakeFirst())
    color = scrapy.Field(output_processor=TakeFirst())
    created_at = scrapy.Field(output_processor=TakeFirst())

class GoodsImageItem(scrapy.Item):
    goods_id = scrapy.Field(output_processor=TakeFirst())
    image_url = scrapy.Field(output_processor=TakeFirst())
    created_at = scrapy.Field(output_processor=TakeFirst())

class GoodsItem(scrapy.Item):
    brand_id = scrapy.Field(output_processor=TakeFirst())
    goods_id = scrapy.Field(output_processor=TakeFirst())
    goods_url = scrapy.Field(output_processor=TakeFirst())
    goods_name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    category_path = scrapy.Field(output_processor=TakeFirst())
    child_category_path = scrapy.Field(output_processor=TakeFirst())
    material = scrapy.Field(output_processor=TakeFirst())
    created_at = scrapy.Field(output_processor=TakeFirst())
    size = scrapy.Field(serializer=GoodsSizeItem)
    color = scrapy.Field(serializer=GoodsColorItem)
    image = scrapy.Field(serializer=GoodsImageItem)


class GoodsLoader(ItemLoader):
    default_item_class = GoodsItem

class GoodsSizeLoader(ItemLoader):
    default_item_class = GoodsSizeItem

class GoodsColorLoader(ItemLoader):
    default_item_class = GoodsColorItem

class GoodsImageLoader(ItemLoader):
    default_item_class = GoodsImageItem