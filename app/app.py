import os, argparse
import time

from flask import render_template, request, send_from_directory

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

logger = stock_api_logger.log_factory().getLogger()


# ------------- Order of defining app, db and importing is important -------------
app = utils.get_flask_app(POSTGRES_USER,
                          POSTGRES_PASSWORD,
                          POSTGRES_HOST,
                          POSTGRES_PORT,
                          POSTGRES_DB,
                          APP_KEY)
from models import db, Stocks  # Require db object
db.init_app(app)





# -------------------------- PAGE VIEW  --------------------------
# -------------------------- PAGE VIEW  --------------------------
@app.route('/', methods=['GET'])
def home():
    return render_template('show_stock.html', stocks=Stocks.query.all())


@app.route("/report")
def report():
    # if os.path.isfile("./static/ec2_report.pdf"):
    #     logger.info("File already exist...: ec2_report.pdf")
    #     return send_from_directory("/home/app/static", "ec2_report.pdf")

    from report import Report
    stock_api = get_stockAPI()
    myreport = Report(stock_api.df)
    myreport.save_chart(fname="./static/ec2_report.pdf")
    myreport.save_chart(fname="./data/ec2_report.pdf")

    return send_from_directory("/home/app/static", "ec2_report.pdf")

@app.route('/download/<companysymbol>')
def report_generic(companysymbol):
    fname = f"{companysymbol}.pdf"
    # if os.path.isfile("./static/" + fname):
    #     logger.info("File already exist...: %s", fname)
    #     return send_from_directory("/home/app/static", fname)

    from report import Report
    stock_api = get_stockAPI(company_symbol=companysymbol)
    myreport = Report(stock_api.df)
    myreport.save_chart(company_symbol=companysymbol, fname="./static/" + fname)
    myreport.save_chart(company_symbol=companysymbol, fname="./data/"   + fname)

    return send_from_directory("/home/app/static", fname)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# -------------------------- PAGE VIEW  --------------------------
# -------------------------- PAGE VIEW  --------------------------




def get_stockAPI(company_symbol: str="AAPL") -> StockAPI:

    stock_api = StockAPI(access_key=STOCK_API_KEY,
                             company_symbol=company_symbol,
                             date_from=args.date_from,
                             date_to=args.date_to)
    stock_api.get_api_result()
    stock_api.api_result_to_dataframe()
    stock_api.save_dataframe_to_csv("data/ec2_generated.csv")

    return stock_api



if __name__ == '__main__':
    logger.info("Safely waiting until DB is setup...")
    time.sleep(5)

    utils.setup_database(app, db)

    stockdb = StockDB(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
    stockdb.connect_db()

    stock_api = get_stockAPI(company_symbol=args.target_company)
    # Need postgresql+psycopg2 for stockdb.engine. Needed for to_sql().
    stock_api.df.to_sql("stocks", stockdb.engine, if_exists='replace', index=False)

    app.run(debug=True, host='0.0.0.0', port=5000)


