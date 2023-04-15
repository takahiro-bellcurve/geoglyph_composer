import os, sys
sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils import dates

from lib.mysql_connector import MysqlConnector
from lib import scrapy_executer

with DAG(
    dag_id="zozotown_brands_goods_8k_scrapy_dag",
    schedule_interval='0 3 * * 1',
    
    default_args={
        "depends_on_past": False,
        "catchup": False,
        'start_date': "2023-03-17",
        "retries": 0,
    },
) as dag:
    
    query = '''
    SELECT brand_id, brand_url, brand_name FROM zozotown_brands LIMIT 7000, 1000
    '''
    db = MysqlConnector()
    brands = db.read(query)

    scrapy_tasks = []
    for brand in brands:
        scraping_zozotown_brand_goods_task = PythonOperator(
            task_id=f"scraping_zozotown_{brand['brand_id']}_goods",
            python_callable=scrapy_executer.run,
            op_kwargs={
                "spider_name": "zozotown_brand_goods",
                "start_url": brand['brand_url'],
                "title": brand['brand_name']
            },
            dag=dag
        )
        scrapy_tasks.append(scraping_zozotown_brand_goods_task)

scrapy_tasks
