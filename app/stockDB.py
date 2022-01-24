import time, sys
import psycopg2
from sqlalchemy import create_engine
import stock_api_logger
logger = stock_api_logger.log_factory().getLogger()

# CONN_STRING = 'postgresql://sunyan:1234@localhost:5432/stockdb'
# DO SOMETHING WITH OS.ENV
# CONN_STRING = f'postgresql://{ADMIN}:{PASSWORD}@localhost:{POSTGRES_PORT}/{DB_NAME}'


class StockDB(object):

    def __init__(self,
                 db_id: str,
                 db_password: str,
                 db_name: str,

                 db_host: str='db',
                 db_port: int=5432,
                 db_type: str='postgresql',
                 db_type_magic = 'postgresql+psycopg2'
                 ):
        logger.info("Creating StockDB...")
        self.conn_string = f'{db_type}://{db_id}:{db_password}@{db_host}:{db_port}/{db_name}'
        # SQLite allows a raw connection for the pd.to_sql, we need to combine with psycopg2.
        self.conn_string_magic = f'{db_type_magic}://{db_id}:{db_password}@{db_host}:{db_port}/{db_name}'
        self.conn_string_masked = f'{db_type}://{db_id}:********@localhost:{db_port}/{db_name}'
        self.db = None
        self.conn = None
        self.cursor = None


    def connect_db(self, trials: int=10):
        logger.info("Connecting to db server %s...", self.conn_string_masked )

        tried = 0
        while(True):
            try:
                tried+=1
                self.db = create_engine(self.conn_string)
                self.engine = create_engine(self.conn_string_magic)

                self.conn = self.db.connect()
                self.conn = psycopg2.connect(self.conn_string)
                self.conn.autocommit = True
                self.cursor = self.conn.cursor()
                break
            except Exception as e:
                logger.info("Waiting connection from db...%s...", self.conn_string_masked)
                logger.info("Error...%s...", e)
                if tried >= trials:
                    sys.exit("Cannot connect to DB:\n" + str(e))
                time.sleep(3)



    # small_df.to_sql('stockhistory', con=conn, if_exists='append',
    #           index=False)

    def exec_query(self, query: str):
        if None in [self.db, self.conn, self.cursor]:
            self.connect_db()
        # self.cursor.execute('''select * from stockhistory;''')
        self.cursor.execute(query)

        try:
            for i in self.cursor.fetchall():
                logger.info(i)
        except: pass

    def show_result(self):
        try:
            for i in self.cursor.fetchall():
                logger.info(i)
        except: print("nothing happened...")


    def store_dataframe_to_sql(self, data_frame, table_name: str):
        data_frame.to_sql(table_name, con=self.conn, if_exists='append', index=False)


    def close_conn(self):
        # conn.commit()
        self.conn.close()

