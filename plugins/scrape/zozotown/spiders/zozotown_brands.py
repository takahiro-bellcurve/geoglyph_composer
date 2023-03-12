import os, sys, datetime

import scrapy
from scrapy.loader import ItemLoader

sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))
from lib.discord_webhook import DiscordWebhook
from scrape.zozotown.items import BrandItem
from scrape.zozotown.custom_spider import CustomSpider


t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')

class ZozotownBrandsSpider(CustomSpider):
    name = "zozotown_brands"
    allowed_domains = ["zozo.jp"]
    start_urls = ["https://zozo.jp/brand/"]

    custom_settings = {
         'ITEM_PIPELINES': {
                'scrape.zozotown.pipelines.ZozotownBrandsPipeline': 300,
            }
    }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = datetime.datetime.now(JST).strftime('%Y/%m/%d %H:%M:%S')
        self.end_time = None
        self.items_scraped = 0
        self.error_count = 0
        self.error_values = []
        self.items = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ZozotownBrandsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        crawler.signals.connect(spider.item_scraped, signal=scrapy.signals.item_scraped)
        crawler.signals.connect(spider.item_error, signal=scrapy.signals.item_error)
        return spider
    
    def spider_closed(self):
        self.end_time = datetime.datetime.now(JST).strftime('%Y/%m/%d %H:%M:%S')
        if self.error_count == 0:
            embeds = [
                {
                    'title': 'ZOZOTOWNのブランド一覧のスクレイピングが完了しました',
                    'description': 
                    f'''
                    spider名: {self.name}

                    開始時刻: {self.start_time}

                    終了時刻: {self.end_time}

                    ブランド情報を{self.items_scraped}件取得しました
                    ''',
                    'color': 15258703
                }
            ]
        else:
            embeds = [
                {
                    'title': 'ZOZOTOWNのブランド一覧のスクレイピングに失敗したItemがありました',
                    'description': 
                    f'''
                    spider名: {self.name}

                    開始時刻: {self.start_time}

                    終了時刻: {self.end_time}

                    ブランド情報を{self.items_scraped}件取得しました

                    エラー件数: {self.error_count}

                    エラー内容: {self.error_values[0:2]}
                    ''',
                    'color': 16711680
                }
            ]
        DiscordWebhook().send(embeds=embeds)


    def item_scraped(self, item):
        self.items_scraped += 1
        item = dict(item)
        item.setdefault("brand_name_kana", "null")
        self.items.append(item)

    def item_error(self, failure):
        self.error_count += 1
        self.error_values.append(failure.value)
        self.logger.error(failure.value)

    

    def parse(self, response):
        brands = response.xpath("//dd[@class='p-brand-list-content']")
        for brand in brands:
            loader = ItemLoader(item=BrandItem(), selector=brand)

            brand_url = brand.xpath(".//a[@class='p-brand-list-content__link']/@href").get()
            loader.add_value("brand_url", f"https://zozo.jp{brand_url}")

            brand_id = brand_url.split("/")[-2]
            loader.add_value("brand_id", brand_id)

            brand_name = brand.xpath("./a/span/text()").get()
            loader.add_value("brand_name", brand_name)

            brand_name_kana = brand.xpath("./a/span/@data-kana").get()
            if not brand_name_kana:
                brand_name_kana = "null"
            loader.add_value("brand_name_kana", brand_name_kana)

            created_at = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
            loader.add_value("created_at", created_at)

            yield loader.load_item()
