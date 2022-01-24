import stock_api_logger
from flask_sqlalchemy import SQLAlchemy

logger = stock_api_logger.log_factory().getLogger()

db = SQLAlchemy()

class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        logger.info("Creating Student table...")
        self.name = name
        self.city = city
        self.addr = addr


# id,date,high,company
# 0,2022-01-14 00:00:00+00:00,173.78,AAPL
# 1,2022-01-13 00:00:00+00:00,176.62,AAPL
# 2,2022-01-12 00:00:00+00:00,177.179,AAPL
class Stocks(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column('date', db.DateTime)
    close = db.Column('high', db.REAL(20))
    volume = db.Column('high', db.BIGINT(30))
    company = db.Column('company', db.String(20))

    def __init__(self, id, date, close, volume,  company):
        logger.info("Creating Student table...")
        self.id = id
        self.date = date
        self.close = close
        self.volume = volume
        self.company = company