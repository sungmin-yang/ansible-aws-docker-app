import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

ACCESS_KEY = "6ca0f0f7528f082e26b191f19f84ff15"
SYMBOL = 'AAPL'
DATE_FROM = '2019-01-08'
DATE_TO = '2022-01-14'
CONN_STRING = 'postgresql://sunyan:1234@localhost:5432/stockdb'
# DO SOMETHING WITH OS.ENV
CONN_STRING = f'postgresql://{ADMIN}:{PASSWORD}@localhost:{POSTGRES_PORT}/{DB_NAME}'

params = {
  'access_key': ACCESS_KEY
}


url  = f'http://api.marketstack.com/v1/eod\
?access_key={ACCESS_KEY}\
&symbols={SYMBOL}\
&date_from={DATE_FROM}\
&date_to={DATE_TO}\
&limit=10000'


api_result = requests.get(url, params)
api_response = api_result.json()


# ------------ Data cleaning ------------
stock_df = pd.DataFrame(api_response['files'])

# Drop NaN columns, which is not the case here.
stock_df.dropna(axis=1, how='all', inplace=True)

# We will keep following columns, [open, high, low,close, volume, adj_close, symbol, exchange, date]
stock_df = stock_df[['open', 'high', 'low', 'close', 'volume', 'adj_close', 'symbol', 'exchange', 'date']]


stock_df = stock_df.astype(dtype={'symbol': 'string',
                                  'exchange': 'string'})
stock_df['date'] = pd.to_datetime(stock_df['date']).dt.strftime('%Y-%m-%d')
stock_df.rename(columns={"symbol": "company"}, inplace=True)

stock_df['id'] = stock_df.index

stock_df.to_csv('aapl.csv', index=False, index_label=False)


# Test
small_df = stock_df[['id', 'date', 'high', 'company']]
small_df.to_csv('small_df.csv', index=False, index_label=False)

small_df = pd.read_csv('small_df.csv', index_col=False)




conn_string = 'postgresql://sunyan:1234@localhost:5432/stockdb'

db = create_engine(conn_string)
conn = db.connect()

# small_df.to_sql('stockhistory', con=conn, if_exists='append',
#           index=False)
conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute('''select * from stockhistory;''')
for i in cursor.fetchall():
    print(i)

# conn.commit()
conn.close()

# engine = create_engine('postgresql://sunyan:1234@localhost:5432/stockdb')
# small_df.to_sql('stockhistory2', engine)


