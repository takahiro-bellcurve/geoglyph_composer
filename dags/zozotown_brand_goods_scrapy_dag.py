import os, sys
sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils import dates

from lib.mysql_connector import MysqlConnector

with DAG(
    dag_id="zozotown_brands_goods_scrapy_dag",
    schedule_interval='30 0 * * 6',
    default_args={
        "depends_on_past": False,
        "catchup": False,
        'start_date': dates.days_ago(8),
    },
) as dag:
    
    query = '''
    SELECT brand_id, brand_url FROM zozotown_brands LIMIT 10, 3
    '''
    db = MysqlConnector()
    brands = db.read(query)

    scrapy_tasks = []
    for brand in brands:
        scraping_zozotown_brand_goods_task = BashOperator(
            task_id=f"scraping_zozotown_{brand['brand_id']}_goods",
            bash_command=f"cd {os.getenv('BASE_DIR')}/plugins/scrape ;  scrapy crawl zozotown_brand_goods -a start_url={brand['brand_url']}",
            dag=dag
        )
        scrapy_tasks.append(scraping_zozotown_brand_goods_task)

scrapy_tasks
