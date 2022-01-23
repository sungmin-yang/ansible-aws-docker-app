import psycopg2
from sqlalchemy import create_engine
import stock_api_logger
logger = stock_api_logger.log_factory().getLogger()

CONN_STRING = 'postgresql://sunyan:1234@localhost:5432/stockdb'
# DO SOMETHING WITH OS.ENV
# CONN_STRING = f'postgresql://{ADMIN}:{PASSWORD}@localhost:{POSTGRES_PORT}/{DB_NAME}'


class StockDB(object):

    def __init__(self,
                 db_id: str,
                 db_password: str,
                 db_name: str,

                 db_ip: str='localhost',
                 db_port: int=5432,
                 db_type: str='postgresql'):
        logger.info("Creating StockDB...")
        self.conn_string = f'{db_type}://{db_id}:{db_password}@{db_ip}:{db_port}/{db_name}'
        self.conn_string_masked = f'{db_type}://{db_id}:********@localhost:{db_port}/{db_name}'
        self.db = None
        self.conn = None
        self.cursor = None

    def connect_db(self):
        logger.info("Connecting to db server %s...", self.conn_string_masked )
        # self.db = create_engine(self.conn_string)
        # self.conn = self.db.connect()
        self.conn = psycopg2.connect(self.conn_string)
        # con = psycopg2.connect(host="localhost", port=5432, dbname="mydb", user="myuser", password="mypwd")

        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

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

