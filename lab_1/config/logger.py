import logging


def get_logger(filename):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(filename)
