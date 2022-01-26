import logging

class StockAPILogger(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        FORMAT = "%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=FORMAT)
        self.logger.setLevel(logging.INFO)

    def getLogger(self) -> logging.Logger:
        if self.logger is not None:
            return self.logger
        else:
            stockAppLogger = StockAPILogger()
            return stockAppLogger

# A factory to return a helper
def log_factory(logger=StockAPILogger()):
    """Example: helper = log_factory().getLogger()"""
    return logger