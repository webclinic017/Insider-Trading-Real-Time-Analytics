from airflow import DAG
from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator

default_args={
    'owner':'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020,4,13),
    'retries':0,
}

dag=DAG(dag_id='insideTrading',default_args=default_args,catchup=False,schedule_interval='30 5 * * 1-5')

consumer = BashOperator(
    task_id='Kafka-Consumer',
    bash_command='./insiderTrading.sh',
    dag=dag,
)


