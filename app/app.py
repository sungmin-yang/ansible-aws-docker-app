import os, json
from flask import render_template, flash, redirect, request, url_for
import pandas as pd

import stock_api_logger
import utils

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
    report.draw_chart(fname="./static/test.png")
    # rendered_chart = report.render_for_html(format="png")

    return render_template("report.html",
                           chart_image="/home/app/static/test.png",
                           best_day=report.get_best_stock_day(),
                           worst_day=report.get_worst_stock_day()
                           )



# @app.route("/graph")
# def graph():
#     sample_df = pd.read_csv(os.getcwd() + '/data/sample.csv', index_col=False).drop('Open', axis=1)
#     chart_data = sample_df.to_dict(orient='records')
#     chart_data = json.dumps(chart_data, indent=2)
#     return render_template("graph.html", data={'chart_data': chart_data})


# @app.route("/graph2")
# def graph2():
#     df = pd.read_csv(os.getcwd() + '/data/big_df.csv', index_col=False)
#     # id, open, high, low, close, volume, adj_close, company, exchange, date
#     # 0, 171.34, 173.78, 171.09, 173.07, 80355000.0, 173.07, AAPL, XNAS, 2022 - 01 - 14 00: 00:00 + 00: 00
#     df = df[[ 'high', 'low', 'close','company','date']]
#     df.rename(columns={"high": "High",
#                        "low": "Low",
#                        "close": "Close",
#                        "company": "Company",
#                        "date": "Date"
#                        }, inplace=True)
#     chart_data = df.to_dict(orient='records')
#     chart_data = json.dumps(chart_data, indent=2)
#     return render_template("graph2.html", data={'chart_data': chart_data,
#                                                 'high_value': json.dumps({"high_day": "2020-01-01"})
#                                                 })


# ---------------------  Web page rendering  END ---------------------
# ---------------------  Web page rendering  END ---------------------
# ---------------------  Web page rendering  END ---------------------



if __name__ == '__main__':
    utils.setup_database(app, db)
    # utils.wait_until_db_setup(db)
    app.run(debug=True, host='0.0.0.0', port=5000)
