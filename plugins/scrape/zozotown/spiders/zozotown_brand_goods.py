import os, sys, datetime, re, logging, json

import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.discord_webhook import DiscordWebhook
from scrape.zozotown.items import GoodsLoader, GoodsSizeLoader, GoodsColorLoader, GoodsImageLoader


t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')

logger = logging.getLogger(__name__)

class ZozotownBrandGoodsSpider(scrapy.spiders.CrawlSpider):
    name = "zozotown_brand_goods"
    allowed_domains = ["zozo.jp"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "scrape.zozotown.pipelines.ZozotownBrandGoodsPipeline": 300,
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_url)

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//li[@class='o-grid-catalog__item']//a[@class='c-catalog-header__link']")), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        logger.warning("parse_item: %s", response.url)
        goods_loader = GoodsLoader(selector=Selector(response))

        brand_id = response.url.split('/')[-4]
        goods_loader.add_value('brand_id', brand_id)

        goods_loader.add_value('goods_url', response.url)

        goods_id = response.url.split('/')[-2]
        goods_loader.add_value('goods_id', goods_id)

        goods_name = response.xpath("//h1[@class='p-goods-information__heading']/text()").get()
        goods_loader.add_value('goods_name', re.sub(r"\s", "", goods_name))

        price = response.xpath("//div[@class='p-goods-information__price']/text()[1]").get()
        discount_price = response.xpath("//div[@class='p-goods-information__price--discount']/text()[1]").get()
        if price:
            pass
        elif discount_price:
            price = discount_price
        else:
            price = "null"
        goods_loader.add_value('price', re.sub(r"\D", "", price))

        description = response.xpath("//div[@class='contbox']//text()").getall()
        if description:
            goods_loader.add_value('description', re.sub(r"\s", "", " ".join(description)))
        else:
            goods_loader.add_value('description', "null")
        category_path = response.xpath("//li[@class='p-goods-information-spec-category-list-item'][1]/a/@href").get()
        goods_loader.add_value('category_path', category_path.split('/')[-2])

        child_category_path = response.xpath("//li[@class='p-goods-information-spec-category-list-item'][2]/a/@href").get()
        if child_category_path:
            goods_loader.add_value('child_category_path', child_category_path.split('/')[-2])
        else:
            goods_loader.add_value('child_category_path', "null")

        material = response.xpath("//dt[contains(text(),'素材')]/following-sibling::dd/text()").get()
        if material:
            goods_loader.add_value('material', material)
        else:
            goods_loader.add_value('material', "null")

        gender = response.xpath("//dt[contains(text(),'性別タイプ')]/following-sibling::dd/a/text()").getall()
        if gender:
            goods_loader.add_value('gender', "-".join(gender))
        else:
            goods_loader.add_value('gender', "null")

        goods_loader.add_value('sizes', self.parse_size(response))
        goods_loader.add_value('colors', self.parse_color(response))
        goods_loader.add_value('images', self.parse_image(response))
        goods_loader.add_value('created_at', datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'))

        yield goods_loader.load_item()

    def parse_color(self, response):
        colors = response.xpath("//dl[@class='p-goods-information-action ']//span[contains(@class,'p-goods-add-cart__color')]/text()").getall()
        for color in colors:
            goods_color_loader = GoodsColorLoader(selector=Selector(response))
            goods_color_loader.add_value('color', color)

            yield goods_color_loader.load_item()

    def parse_image(self, response):
        images = response.xpath("//li[@class='p-goods-thumbnail-list__item']//img/@src").getall()
        for image in images:
            goods_image_loader = GoodsImageLoader(selector=Selector(response))
            goods_image_loader.add_value('image_url', re.sub("35.", "500.", image))

            yield goods_image_loader.load_item()

    def parse_size(self, response):
        sizes_blocks = response.xpath("//div[@class='p-goods-size-scroll-table-column-left']//tbody[@class='p-goods-size-table-body']/tr")
        for size_block in sizes_blocks:
            goods_size_loader = GoodsSizeLoader(selector=Selector(response))

            size = size_block.xpath("./th/@data-size").get()
            goods_size_loader.add_value('size', size)

            info_label = size_block.xpath("./td/@data-label").getall()
            info_value = size_block.xpath("./td/text()").getall()
            info = {}
            for label, value in zip(info_label, info_value):
                info[label] = value.strip()
            goods_size_loader.add_value('info', json.dumps(info, ensure_ascii=False, indent=2))

            yield goods_size_loader.load_item()

