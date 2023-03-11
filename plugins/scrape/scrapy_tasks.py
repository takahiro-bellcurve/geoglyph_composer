import os, sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../sodashi-default-service-account.json"


PROCESS = CrawlerProcess(get_project_settings())

def scraping_zozotown_brands():
    PROCESS.crawl('zozotown_brands')
    PROCESS.start()