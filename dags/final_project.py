from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator
from helpers.final_project_sql_statements import SqlQueries


default_args = {
    'owner': 'ELJANDOUBI',
    'start_date': pendulum.now(),
    'catchup':False,
    "depends_on_past":False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table='staging_events',
        s3_bucket='bean-murdock',
        s3_key='log-data',
        region='us-east-1',
        copy_options='s3://bean-murdock/log_json_path.json'
    )


    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table='staging_songs',
        s3_bucket='bean-murdock',
        s3_key='song-data',
        region='us-east-1',
        copy_options='auto'
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table', 
        redshift_conn_id = 'redshift',
        table = 'songplays',
        sql = SqlQueries.songplay_table_insert
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id='redshift',
        table='users',
        sql=SqlQueries.user_table_insert,
        insert_mode='with truncate'
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id='redshift',
        table='songs',
        sql=SqlQueries.song_table_insert,
        insert_mode='with truncate'
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id='redshift',
        table='artists',
        sql=SqlQueries.artist_table_insert,
        insert_mode='with truncate'
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id='redshift',
        table='time',
        sql=SqlQueries.time_table_insert,
        insert_mode='with truncate'
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        check_stmts=[
            {
                'sql': 'SELECT COUNT(*) FROM songplays;',
                'op': 'gt',
                'val': 0
                },
            {
                'sql': 'SELECT COUNT(*) FROM songplays WHERE song_id IS NULL;',
                'op': 'eq',
                'val': 0
                }
            ]
    )

    end_operator = DummyOperator(task_id='End_execution')

    # graph

    start_operator >> [ stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table >> [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table
        ] >> run_quality_checks >> end_operator

    

final_project_dag = final_project()