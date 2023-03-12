import scrapy
import logging
from logging import StreamHandler, Formatter

class CustomSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        # その他設定を継承
        super().__init__(*args, **kwargs)
        # 指定したハンドラが出力するログのレベルをINFOに上書き
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        # ログのフォーマットの設定
        handler_format = Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s', datefmt='%Y/%d/%m %I:%M:%S')
        stream_handler.setFormatter(handler_format)
        # 各ハンドラに設定を反映
        stat_logger = logging.getLogger('scrapy.statscollectors')
        stat_logger.addHandler(stream_handler)
        scrape_logger = logging.getLogger('scrapy.core.scraper')
        scrape_logger.addHandler(stream_handler)
        # 各spider_nameを名前に持つハンドラから、スクレイピング開始をロギングする
        start_logger = logging.getLogger(__name__)
        start_logger.addHandler(stream_handler)
        start_logger.info('scrapy started')
       

class CustomCrawlSpider(scrapy.spiders.CrawlSpider):
    def __init__(self, *args, **kwargs):
        # その他設定を継承
        super().__init__(*args, **kwargs)
        # 指定したハンドラが出力するログのレベルをINFOに上書き
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        # ログのフォーマットの設定
        handler_format = Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s', datefmt='%Y/%d/%m %I:%M:%S')
        stream_handler.setFormatter(handler_format)
        # 各ハンドラに設定を反映
        stat_logger = logging.getLogger('scrapy.statscollectors')
        stat_logger.addHandler(stream_handler)
        scrape_logger = logging.getLogger('scrapy.core.scraper')
        scrape_logger.addHandler(stream_handler)
        # 各spider_nameを名前に持つハンドラから、スクレイピング開始をロギングする
        start_logger = logging.getLogger(__name__)
        start_logger.addHandler(stream_handler)
        start_logger.info('scrapy started')
        