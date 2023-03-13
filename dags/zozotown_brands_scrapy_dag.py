import os, sys
sys.path.append(os.path.join(os.getenv("BASE_DIR"), "plugins"))

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from lib.discord_webhook import DiscordWebhook

with DAG(
    dag_id="zozotown_brands_scrapy_dag",
    schedule_interval='0 0 * * 6',
    default_args={
        "depends_on_past": False,
        "catchup": False,
        "start_date": "2023-3-01",
    },
) as dag:

    scraping_zozotown_brands_task = BashOperator(
        task_id="scraping_zozotown_brands",
        bash_command=f"cd {os.getenv('BASE_DIR')}/plugins/scrape ;  scrapy crawl zozotown_brands",
        dag=dag
    )


scraping_zozotown_brands_task