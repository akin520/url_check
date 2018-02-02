import logging
import os
from logging.handlers import TimedRotatingFileHandler


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class Logs(object):
    logfile = os.path.join(os.getcwd() + '/', 'log/log.log')
    if not os.path.exists(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = TimedRotatingFileHandler(logfile, 'midnight', backupCount=15)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    logger.addHandler(file_handler)
