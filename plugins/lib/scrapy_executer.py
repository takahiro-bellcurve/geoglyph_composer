import os, sys, subprocess

def run(spider_name, start_url, title):
    BASE_DIR = os.getenv("BASE_DIR")
    scrapy_log = subprocess.run(
        [f"cd {BASE_DIR}/plugins/scrape/ ;  scrapy crawl {spider_name} -a start_url={start_url} -a title={title}"]
    ,shell=True,text=True,capture_output=True).stderr
    print(scrapy_log)
    error_count = scrapy_log.count('ERROR')
    if error_count > 0:
        raise ValueError(f"{error_count} errors found in scrapy output")