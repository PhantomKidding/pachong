#-*-coding:utf-8-*-
__author__ = 'cchen'

import logging
import sys
from datetime import datetime

from pytz import timezone, utc


class Logger(object):
    def __init__(self, filepath, filemode='a', tz='US/Central'):
        def central_time(*args):
            utc_dt = utc.localize(datetime.utcnow())
            my_tz = timezone(tz)
            converted = utc_dt.astimezone(my_tz)
            return converted.timetuple()

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(message)s',
            # format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=filepath,
            filemode=filemode)
        logging.Formatter.converter = central_time
        self.logger = logging.getLogger(__name__)

    def push(self, job, message):
        self.logger.info('[{}]: {}'.format(job, message))
