FROM apache/airflow:2.5.1-python3.9
USER airflow
COPY requirements.txt /
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt