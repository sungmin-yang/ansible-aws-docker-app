import requests
import pandas as pd
import json
import stock_api_logger

logger = stock_api_logger.log_factory().getLogger()


class StockAPI(object):
    def __init__(self, access_key: str,
                        company_symbol: str,
                        date_from: str,
                        date_to: str,
                        ):
        self.access_key = access_key
        self.company_symbol = company_symbol
        #supported date formats: Y - m - d, Y - m - d H: i:s & ISO - 8601(Y - m - d\\TH: i:sO)
        self.date_from = date_from
        self.date_to = date_to
        self.request_url = f'http://api.marketstack.com/v1/eod\
?access_key={access_key}\
&symbols={company_symbol}\
&date_from={date_from}\
&date_to={date_to}\
&limit=10000'
        self.params = {'access_key': access_key }

        self.api_result = None
        self.api_response = None
        self.df = None
        self.conn_string = None


    def get_api_result(self) -> json:
        logger.info('Requesting API to get Stock data...')
        logger.info('Using URL: %s', self.request_url)
        self.api_result = requests.get(self.request_url, self.params)
        self.api_response = self.api_result.json()
        logger.info('API response: %s', self.api_result)
        return self.api_response


    def api_result_to_dataframe(self) -> pd.DataFrame:
        logger.info('Transforming api result (json) to pandas.DataFrame.')
        self.df = pd.DataFrame(self.api_response['data'])

        # Drop NaN columns, which is not the case here.
        self.df.dropna(axis=1, how='all', inplace=True)
        # Select columns we want
        self.df = self.df[['date', 'close', 'volume', 'symbol']]

        # Cleaning
        self.df = self.df.astype(dtype={'symbol': 'string'})
        self.df.rename(columns={"symbol": "company"}, inplace=True)
        self.df['date'] = pd.to_datetime(self.df['date']).dt.strftime('%Y-%m-%d')

        return self.df

    def save_dataframe_to_csv(self, path: str="data/100rows.csv") -> None:
        logger.info('Saving dataframe to %s', path)
        self.df.to_csv(path, index=False, index_label=False)

    def read_csv_to_dataframe(self, path: str="data/100rows.csv") -> None:
        logger.info('Reading csv file into DataFrame from %s', path)
        self.df.read_csv(path, index_col=False)