import os

import pandas as pd
import matplotlib.pyplot as plt
import stock_api_logger
from io import BytesIO
import base64

class Report(object):
    MAX_X_AXIS_NUMBER = 6


    def __init__(self, cleaned_dataframe: pd.DataFrame):
        self.logger = stock_api_logger.log_factory().getLogger()
        self.logger.info("Creating Report...")

        self.df = cleaned_dataframe
        self.sort_by_date()

        self.best_day = self.get_best_stock_day()
        self.worst_day = self.get_worst_stock_day()


    def sort_by_date(self):
        self.df.sort_values(by='date', ascending=True, inplace=True)

    def find_highest_stock_value_date(self) -> (float, str):
        highest_value = self.df["close"].max()
        higest_date   = self.df['date'][self.df["close"] == highest_value].values[0]
        # best_stock_day = self.df[self.df["close"] == self.df["close"].max()].date.values[0]
        return (highest_value, higest_date)

    def find_lowest_stock_value_date(self) -> (float, pd._libs.tslibs.timestamps.Timestamp):
        lowest_value = self.df["close"].min()
        lowest_date   = self.df['date'][self.df["close"] == lowest_value].values[0]
        # best_stock_day = self.df[self.df["close"] == self.df["close"].max()].date.values[0]
        return (lowest_value, lowest_date)

    def get_worst_stock_day(self) -> str:
        _, worst_day = self.find_lowest_stock_value_date()
        self.logger.info("get_worst_stock_day: %s",  worst_day)
        return worst_day

    def get_best_stock_day(self) -> str:
        _, best_day = self.find_highest_stock_value_date()
        self.logger.info("get_best_stock_day: %s", best_day)
        return best_day

    def get_amount_stored_data(self) -> int:
        return self.df.shape[0]

    def draw_chart(self, fname: str='chart.png') -> None:
        self.logger.info("Drawing report chart...")
        # Setting Top chart (Stock closed price)
        top_plt = plt.subplot2grid((5,4), (0, 0), rowspan=3, colspan=4)
        top_plt.plot(self.df['date'], self.df["close"])

        ymax, xmax = self.find_highest_stock_value_date()
        ymin, xmin = self.find_lowest_stock_value_date()

        # Limit the number of X-axis values to 6
        ax = plt.gca()
        ax.xaxis.set_major_locator(plt.MaxNLocator(self.MAX_X_AXIS_NUMBER))

        plt.annotate(f'Higest - {self.best_day}', xy=(xmax, ymax), xytext=(xmax, ymax + 15),
                     arrowprops=dict(facecolor='black', shrink=0.05),)
        plt.annotate(f'Lowest - {self.worst_day}', xy=(xmin, ymin + 5), xytext=(xmin, ymin + 20),
                     arrowprops=dict(facecolor='black', shrink=0.05),)
        plt.title('Historical stock prices of Apple.')


        # Drawing second chart, number of trading volumn.
        bottom_plt = plt.subplot2grid((5, 4), (3, 0), rowspan=10, colspan=40)  # hspace = 0.5
        bottom_plt.bar(self.df.index, self.df['volume'])

        plt.subplots_adjust(bottom=.10, top=.85, hspace=1)

        plt.title('\nTrading Volume', y=-0.6)
        plt.gcf().set_size_inches(12, 8)

        self.logger.info("Current dir: " + os.getcwd())
        self.logger.info("Saving report chart...:" + os.path.join(os.getcwd(), fname))
        plt.savefig(fname)


    # def render_for_html(self, format:str='png') -> base64.b64encode:
    #     ### Rendering Plot in Html
    #     figfile = BytesIO()
    #     plt.savefig(figfile, format=format)
    #     figfile.seek(0)
    #     figdata_png = base64.b64encode(figfile.getvalue())
    #     return figdata_png

    def send_chart(self):
        return None
        # strIO = StringIO.StringIO()
        # plt.savefig(strIO, dpi=fig.dpi)
        # strIO.seek(0)
        # return strIO
        #
        # strIO = using_matplotlib()
        # return send_file(strIO, mimetype='image/png')




