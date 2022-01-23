import os, json
from flask import render_template, flash, redirect, request, url_for
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
APP_KEY
)


SAMPLE_N_ROWS = 30
logger = stock_api_logger.log_factory().getLogger()



# ---------------------  Model(Table) is dependent on above methods ---------------------
app = utils.get_flask_app(POSTGRES_USER,
                          POSTGRES_PASSWORD,
                          POSTGRES_HOST,
                          POSTGRES_PORT,
                          POSTGRES_DB,
                          APP_KEY)

from models import db, Students  # Require db object
db.init_app(app)




# ---------------------  Web page rendering  START ---------------------
# ---------------------  Web page rendering  START ---------------------
# ---------------------  Web page rendering  START ---------------------
@app.route('/', methods=['GET', 'POST'])
def home():



    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(
                request.form['name'],
                request.form['city'],
                request.form['addr'])
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('home'))
    return render_template('show_all.html', students=Students.query.all())



# @app.route('/test', methods=['GET', 'POST'])
# def test():
#
#     stock = Stocks.create_stocks_table(
#         request.form['id'],
#         request.form['date'],
#         request.form['high'],
#         request.form['company'])
#
#     if request.method == 'POST':
#         if not request.form['company']:
#             flash('Please enter all the fields', 'error')
#         else:
#             db.session.add(stock)
#             db.session.commit()
#             flash('Company was successfully found')
#             return redirect(url_for('test'))
#
#     return render_template('show_stock.html', students=stock.get_model.query.all())




small_df = pd.read_csv(os.getcwd() + '/data/small_df.csv', index_col=False)
@app.route('/test2', methods=['GET'])
def test2():
    return small_df.head(SAMPLE_N_ROWS).to_html(index=False)



@app.route("/report")
def report():
    from generate_report import Report
    sample_df = pd.read_csv(os.getcwd() + '/data/big_df.csv', index_col=False)
    report = Report(sample_df)
    report.draw_chart(fname="./static/testt.png")
    # rendered_chart = report.render_for_html(format="png")

    return render_template("report.html",
                           chart_image="/home/app/static/testt.png",
                           best_day=report.get_best_stock_day(),
                           worst_day=report.get_worst_stock_day()
                           )



# ---------------------  Web page rendering  END ---------------------
# ---------------------  Web page rendering  END ---------------------
# ---------------------  Web page rendering  END ---------------------



if __name__ == '__main__':
    utils.setup_database(app, db)


    stock_api = StockAPI(access_key='6ca0f0f7528f082e26b191f19f84ff15',
                         company_symbol='AAPL', date_from='2019-01-08', date_to='2022-01-14')
    stock_api.get_api_result()
    stock_api.transform_to_dataframe()

    stockdb = StockDB(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
    stockdb.connect_db()
    stockdb.exec_query('''select * from stockhistory;''')



    # utils.wait_until_db_setup(db)
    app.run(debug=True, host='0.0.0.0', port=5000)
