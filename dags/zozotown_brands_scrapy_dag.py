import os, sys
sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from lib import scrapy_executer

with DAG(
    dag_id="zozotown_brands_scrapy_dag",
    schedule_interval='0 0 * * 6',
    default_args={
        "depends_on_past": False,
        "catchup": False,
        "start_date": "2023-3-01",
    },
) as dag:

    scraping_zozotown_brands_task = PythonOperator(
        task_id="scraping_zozotown_brands",
        python_callable=scrapy_executer.run,
        op_kwargs={
            "spider_name": "zozotown_brands",
            "start_url": "https://zozo.jp/brand/",
            "title": "zozotown_brands"
        },
        dag=dag
    )


scraping_zozotown_brands_task