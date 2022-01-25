import stock_api_logger
from flask_sqlalchemy import SQLAlchemy

logger = stock_api_logger.log_factory().getLogger()

db = SQLAlchemy()


# id,date,close,volume,company
# 1,2022-01-14,173.07,80355000,AAPL
# 2,2022-01-13,172.19,81572060,AAPL
# 3,2022-01-12,175.53,70577429,AAPL
# 4,2022-01-11,175.08,76015600,AAPL
class Stocks(db.Model):
    date = db.Column('date', db.DATE, primary_key=True)
    close = db.Column('close', db.REAL(20))
    volume = db.Column('volume', db.BIGINT())
    company = db.Column('company', db.String(20))

    def __init__(self, date, close, volume,  company):
        logger.info("Creating Student table...")
        self.date = date
        self.close = close
        self.volume = volume
        self.company = company