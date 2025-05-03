from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import text
from app.infrastructure.airflow.dags.postgres_sync import get_db
from app.infrastructure.airflow.dags.utils.walk_test_status_enum import WalkTestStatusEnum


def create_update_walk_test_status_dag(walk_test_id: str, walk_test_status_id: WalkTestStatusEnum) -> DAG:
    # Replace these with your actual DB credentials or use Airflow Connections

    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }
    start_date = datetime.now() + timedelta(hours=72)  # Adjust as needed

    dag = DAG(
        dag_id=f'update_walk_test_status_dag_{walk_test_id}',
        default_args=default_args,
        description=f'Marks walk test as {walk_test_status_id} 72 hours after creation',
        schedule_interval=None,
        start_date=start_date,
        catchup=False,
        tags=['walk_test'],
    )

    def wrapper(**kwargs):
        walk_test_id = kwargs['dag_run'].conf.get('walk_test_id')
        walk_test_status_id = kwargs['dag_run'].conf.get('walk_test_status_id')
        update_walk_test_as_deprecated(walk_test_id, walk_test_status_id)

    PythonOperator(
        task_id='mark_status_deprecated',
        python_callable=wrapper,
        provide_context=True,
        dag=dag,
    )
    print(f'dag{dag} with walk_test_id {walk_test_id} is started to be marked as deprecated in 72 hours')

    return dag

def update_walk_test_as_deprecated(walk_test_id: str, walk_test_status_id: WalkTestStatusEnum) -> None:
        db = get_db()  # Synchronous DB session

        try:
            # Execute the SQL command
            db.execute(text("""
                UPDATE table_walk_test
                SET walk_test_status_id = :walk_test_status
                WHERE walk_test_id = :walk_test_id
            """), {"walk_test_status": walk_test_status_id, "walk_test_id": walk_test_id})

            # Commit the transaction
            db.commit()

        except Exception as e:
            print(f"Error occurred while updating walk test status: {e}")
            db.rollback()  # Rollback if something goes wrong

        finally:
            db.close()  # Close the session
