import datetime as dt
from time import sleep

from .fetch import fetch_and_save_events
from .local_config import SOURCES, REFRESH_TIMES
from .utils import get_now, logger, DATE_FORMAT
from .website import update_website


def next_run_time(time: dt.time):
    now = get_now()
    target = dt.datetime.combine(now.date(), time).replace(tzinfo=now.tzinfo)
    if target <= now:
        target += dt.timedelta(days=1)
    return target


def update():
    for source in SOURCES:
        logger.info(f'Updating {source.name}')
        fetch_and_save_events(source=source)
    update_website(sources=SOURCES)


while True:
    try:
        logger.info('Updating...')
        update()
    except Exception as e:
        logger.error('An error occurred while updating:', exc_info=e)
    target = min([next_run_time(t) for t in REFRESH_TIMES])
    logger.info(f'Sleeping until {target.strftime(DATE_FORMAT)}')
    sleep((target - get_now()).total_seconds())