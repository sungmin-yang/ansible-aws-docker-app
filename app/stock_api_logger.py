import logging

class StockAPILogger(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        FORMAT = "%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=FORMAT)
        self.logger.setLevel(logging.INFO)
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # ch.setFormatter(formatter)
        # self.helper.addHandler(ch)

        # make a handler
        # handler = logging.StreamHandler()
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)

        # add it to the root helper
        # logging.getLogger().addHandler(handler)


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