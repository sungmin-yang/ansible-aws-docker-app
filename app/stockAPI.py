import requests
import pandas as pd
import json

ACCESS_KEY = "6ca0f0f7528f082e26b191f19f84ff15"
SYMBOL = 'AAPL'
DATE_FROM = '2019-01-08'
DATE_TO = '2022-01-14'
# DO SOMETHING WITH OS.ENV

params = {
  'access_key': ACCESS_KEY
}


url  = f'http://api.marketstack.com/v1/eod\
?access_key={ACCESS_KEY}\
&symbols={SYMBOL}\
&date_from={DATE_FROM}\
&date_to={DATE_TO}\
&limit=10000'



class StockAPI(object):
    def __init__(self, access_key: str,
                        company_symbol: str,
                        date_from: str,
                        date_to: str,
                        ):
        self.access_key = access_key
        self.company_symbol = company_symbol
        self.date_from = date_from
        self.date_to = date_to
        self.request_url = url  = f'http://api.marketstack.com/v1/eod\
?access_key={ACCESS_KEY}\
&symbols={SYMBOL}\
&date_from={DATE_FROM}\
&date_to={DATE_TO}\
&limit=10000'
        self.params = {'access_key': access_key }

        self.api_result = None
        self.api_response = None
        self.df = None
        self.conn_string = None


    def get_api_result(self) -> json:
        self.api_result = requests.get(self.request_url, params)
        self.api_response = self.api_result.json()
        return self.api_response

    def get_result_dataframe(self) -> pd.DataFrame:
        if self.api_response == None or self.df == None:
            self.get_api_result()
            self.transform_to_dataframe()
        return self.df

    def transform_to_dataframe(self) -> pd.DataFrame:
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
        self.df.to_csv(path, index=False, index_label=False)

    def read_dataframe_to_csv(self, path: str="data/100rows.csv") -> None:
        self.df.read_csv(path, index_col=False)