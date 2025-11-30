import datetime as dt
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from zoneinfo import ZoneInfo


ET = ZoneInfo('America/New_York')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_MS = '%Y-%m-%d %H:%M:%S.%f'


class ETFormatter(logging.Formatter):
    def converter(self, timestamp):
        return dt.datetime.fromtimestamp(timestamp, ET)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        return dt.strftime(DATE_FORMAT_MS)[:-3]


def setup_logger(*, log_path=None, backup_count=7):
    if log_path is None:
        log_path = Path(__file__).resolve().parent / 'logs/economics_calendars.log'
    handler = TimedRotatingFileHandler(
        log_path,
        when='midnight',
        interval=1,
        backupCount=backup_count,
        utc=False
    )

    fmt = '%(asctime)s | %(levelname)s | %(message)s'
    handler.setFormatter(ETFormatter(fmt))

    logger = logging.getLogger('economics_calendars')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


logger = setup_logger()
get_now = lambda: dt.datetime.now(ZoneInfo('America/New_York'))
