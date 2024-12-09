FROM apache/airflow:2.10.3-python3.12
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
RUN pip install -r /opt/airflow/plugins/requirements.txt
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__EXECUTOR=SequentialExecutor
RUN airflow db init && \
    airflow users create \
    --username airflow \
    --firstname Firstname \
    --lastname Lastname \
    --email admin@example.com \
    --role Admin \
    --password airflow
#RUN chmod -R 755 /opt/airflow/plugins