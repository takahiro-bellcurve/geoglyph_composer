FROM apache/airflow:2.5.1
ENV BASE_DIR=/opt/airflow

USER root

RUN mkdir -p /opt/airflow/logs && \
    mkdir -p /opt/airflow/dags && \
    mkdir -p /opt/airflow/plugins 

RUN chmod -R 777 /opt/airflow
RUN chmod -R 777 /opt/airflow/logs

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    libleveldb-dev

USER airflow
COPY requirements.txt /
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt