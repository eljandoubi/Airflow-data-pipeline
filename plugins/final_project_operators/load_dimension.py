from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    insert_sql = """
        INSERT INTO {}
        {};
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql="",
                 insert_mode="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)     
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.insert_mode = insert_mode

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id)
        if self.insert_mode == 'with truncate':
            self.log.info(f'Truncate and insert data into dimension table: {self.table}') 
            redshift.run(f'TRUNCATE TABLE {self.table}')  
        else:          
            self.log.info(f'Insert data into dimension table: {self.table}')         
        
        formatted_sql = LoadDimensionOperator.insert_sql.format(
            self.table,
            self.sql
        )
        redshift.run(formatted_sql)