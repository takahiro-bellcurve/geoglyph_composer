FROM apache/airflow:2.5.1
ENV BASE_DIR=/opt/airflow

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    libleveldb-dev

USER airflow
COPY requirements.txt /
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt