import pandas as pd
import matplotlib.pyplot as plt
import uuid
from datetime import datetime


class Report(object):
    MAX_X_AXIS_NUMBER = 6

    def __init__(self, cleaned_dataframe: pd.DataFrame):
        self.df = cleaned_dataframe
        self.sort_by_date()

    def sort_by_date(self):
        self.df.sort_values(by='date', ascending=True, inplace=True)

    def find_highest_stock_value_date(self) -> (float, str):
        highest_value = self.df["close"].max()
        higest_date = self.df['date'][self.df["close"] == highest_value].values[0]
        # best_stock_day = self.df[self.df["close"] == self.df["close"].max()].date.values[0]
        return (highest_value, higest_date)

    def find_lowest_stock_value_date(self) -> (float, pd._libs.tslibs.timestamps.Timestamp):
        lowest_value = self.df["close"].min()
        lowest_date = self.df['date'][self.df["close"] == lowest_value].values[0]
        # best_stock_day = self.df[self.df["close"] == self.df["close"].max()].date.values[0]
        return (lowest_value, lowest_date)

    def get_worst_stock_day(self) -> str:
        _, worst_day = self.find_lowest_stock_value_date()
        return worst_day

    def get_best_stock_day(self) -> str:
        _, best_day = self.find_highest_stock_value_date()
        return best_day

    def get_amount_stored_data(self) -> int:
        return self.df.shape[0]

    def draw_chart(self, company_name: str = "AAPL") -> None:

        ymax, xmax = self.find_highest_stock_value_date()
        ymin, xmin = self.find_lowest_stock_value_date()
        best_stock_day = self.get_best_stock_day()
        worst_stock_day = self.get_worst_stock_day()

        fig, axs = plt.subplots(3, 1, constrained_layout=False)
        #         fig.tight_layout()
        #         fig = plt.figure(dpi=150)

        # Saving suptitle and pass it to save_chart() because it does not appear in png, pdf files
        self.suptitle = fig.suptitle(f'Report: Financial information of [{company_name}]\n',
                                     fontsize=28,
                                     horizontalalignment="center",
                                     y=1.12)

        # Main chart
        axs[0].plot(self.df['date'], self.df["close"])
        axs[0].set_title('Stock chart')
        axs[0].set_xlabel('Date')
        axs[0].set_ylabel('USD$')

        axs[0].xaxis.set_major_locator(plt.MaxNLocator(self.MAX_X_AXIS_NUMBER))
        axs[0].annotate(f'Higest - {best_stock_day}', xy=(xmax, ymax), xytext=(xmax, ymax + 18), color='red',
                        arrowprops=dict(facecolor='black', shrink=0.05), )
        axs[0].annotate(f'Lowest - {worst_stock_day}', xy=(xmin, ymin + 5), xytext=(xmin, ymin + 22), color='blue',
                        arrowprops=dict(facecolor='black', shrink=0.05), )

        # Adding margin.
        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.9,
                            top=0.9,
                            wspace=0.4,
                            hspace=0.4)

        # volume chart
        axs[1].bar(self.df.index, self.df['volume'])
        axs[1].set_title('volume of trading')
        axs[1].set_xlabel('Date')
        axs[1].set_ylabel('Number of stocks')

        # Table for best & worst days + amount of data
        table_data = [
            ["best day", self.get_best_stock_day()],
            ["worst day", self.get_worst_stock_day()],
            ["amount stored data", self.get_amount_stored_data()]
        ]
        ax = axs[2]
        table = ax.table(cellText=table_data, loc='best', cellLoc='center')
        table.set_fontsize(14)
        ax.axis('off')
        axs[2] = table

        # Adding margin.
        plt.subplots_adjust(bottom=0.02)

        # Adding document id and generated time.
        id_and_time = "ID: {}  Time: {}".format(str(uuid.uuid4()), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        plt.text(1,
                 -0.02,
                 id_and_time,
                 verticalalignment="bottom",
                 horizontalalignment='right',
                 wrap=True,
                 fontsize=12)

        fig = plt.gcf()
        fig.set_size_inches(14, 10)

    def save_chart(self, fname: str="./static/chart.pdf") -> None:
        self.draw_chart()
        chart_type = fname.split(".")[-1]
        if chart_type == "pdf":
            plt.savefig(fname, bbox_inches='tight', pad_inches=1, bbox_extra_artists=[self.suptitle])
        else:
            plt.savefig(fname)











