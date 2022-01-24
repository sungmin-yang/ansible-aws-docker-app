import os, argparse
import time

from flask import render_template, flash, redirect, request, url_for, send_from_directory
import pandas as pd

import stock_api_logger
import utils
from stockDB import StockDB
from stockAPI import StockAPI

from constants import (
POSTGRES_USER,
POSTGRES_PASSWORD,
POSTGRES_HOST,
POSTGRES_PORT,
POSTGRES_DB,
APP_KEY,
STOCK_API_KEY
)

# Get three args {{ TARGET_COMPANY }} {{ DATE_FROM }} {{ DATE_TO }}
parser = argparse.ArgumentParser()
parser.add_argument("-C", "--target_company", help="Type company name that you want to get stock info", required=True)
parser.add_argument("-F", "--date_from", help="Type date from", required=True)
parser.add_argument("-T", "--date_to", help="Type date to", required=True)
args = parser.parse_args()




SAMPLE_N_ROWS = 30
logger = stock_api_logger.log_factory().getLogger()



# ---------------------  Model(Table) is dependent on above methods ---------------------
app = utils.get_flask_app(POSTGRES_USER,
                          POSTGRES_PASSWORD,
                          POSTGRES_HOST,
                          POSTGRES_PORT,
                          POSTGRES_DB,
                          APP_KEY)

from models import db, Students, Stocks  # Require db object
db.init_app(app)




# ---------------------  Web page rendering  START ---------------------
# ---------------------  Web page rendering  START ---------------------
# ---------------------  Web page rendering  START ---------------------
# @app.route('/', methods=['GET', 'POST'])
# def home():
#
#
#
#     if request.method == 'POST':
#         if not request.form['name'] or not request.form['city'] or not request.form['addr']:
#             flash('Please enter all the fields', 'error')
#         else:
#             student = Students(
#                 request.form['name'],
#                 request.form['city'],
#                 request.form['addr'])
#             db.session.add(student)
#             db.session.commit()
#             flash('Record was successfully added')
#             return redirect(url_for('home'))
#     return render_template('show_all.html', students=Students.query.all())


@app.route('/', methods=['GET'])
def home():
    return render_template('show_stock.html', stocks=Stocks.query.all())


# @app.route('/test', methods=['GET', 'POST'])
# def test():
#
#     stockdb = StockDB(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
#     stockdb.connect_db()
#     # Check existing tables
#     stockdb.exec_query("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
#     stockdb.exec_query('''select * from stocks;''')
#
#     return render_template('show_stock.html')




# small_df = pd.read_csv(os.getcwd() + '/data/small_df.csv', index_col=False)
# @app.route('/test2', methods=['GET'])
# def test2():
#     return small_df.head(SAMPLE_N_ROWS).to_html(index=False)



@app.route("/report")
def report():
    from report import Report
    # sample_df = pd.read_csv(os.getcwd() + '/data/big_df.csv', index_col=False)
    # myreport = Report(sample_df)

    if os.path.isfile("./static/ec2_report.pdf"):
        return send_from_directory("/home/app/static", "ec2_report.pdf")

    stock_api = get_stockAPI()
    myreport = Report(stock_api.df)
    myreport.save_chart(fname="./static/ec2_report.pdf")
    myreport.save_chart(fname="./data/ec2_report.pdf")

    return send_from_directory("/home/app/static", "ec2_report.pdf")


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def get_stockAPI() -> StockAPI:
    stock_api = StockAPI(access_key=STOCK_API_KEY,
                         company_symbol=args.target_company,
                         date_from=args.date_from,
                         date_to=args.date_to)
    stock_api.get_api_result()
    stock_api.transform_to_dataframe()
    stock_api.save_dataframe_to_csv("data/ec2_generated.csv")
    return stock_api


# ---------------------  Web page rendering  END ---------------------
# ---------------------  Web page rendering  END ---------------------
# ---------------------  Web page rendering  END ---------------------



if __name__ == '__main__':
    logger.info("Safely waiting until DB is setup...")
    time.sleep(5)

    utils.setup_database(app, db)

    stockdb = StockDB(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
    stockdb.connect_db()

    stock_api = get_stockAPI()
    # Need postgresql+psycopg2 for stockdb.engine. Needed for to_sql().
    stock_api.df.to_sql("stocks", stockdb.engine, if_exists='append', index=False)

    app.run(debug=True, host='0.0.0.0', port=5000)


