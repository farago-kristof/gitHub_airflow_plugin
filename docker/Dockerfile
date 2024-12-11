FROM apache/airflow:2.10.3-python3.12
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__EXECUTOR=SequentialExecutor
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    default-libmysqlclient-dev \
    && apt-get clean
USER airflow
COPY ./ /opt/airflow/plugins
RUN pip install --no-cache-dir -r /opt/airflow/plugins/requirements.txt
RUN airflow db init
RUN airflow users create \
    --username airflow \
    --firstname Firstname \
    --lastname Lastname \
    --email admin@example.com \
    --role Admin \
    --password airflow