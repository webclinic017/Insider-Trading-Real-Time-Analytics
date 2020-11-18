from airflow import DAG
from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator

default_args={
    'owner':'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020,4,13),
    'retries':0,
}

dag=DAG(dag_id='insiderBuying',default_args=default_args,catchup=False,schedule_interval='30 5 * * 1-5')

buying = BashOperator(
    task_id='Kafka-Producer1',
    bash_command='./insiderBuying.sh',
    dag=dag,
)



