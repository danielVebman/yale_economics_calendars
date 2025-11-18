import datetime as dt
from time import sleep

from .fetch import fetch_and_save_events
from .local_config import SOURCES, REFRESH_TIMES
from .utils import get_now
from .website import update_website


def next_run_time(time: dt.time):
    now = get_now()
    target = dt.datetime.combine(now.date(), time).replace(tzinfo=now.tzinfo)
    if target <= now:
        target += dt.timedelta(days=1)
    return target


def loop():
    for source in SOURCES:
        fetch_and_save_events(source=source)
    update_website(sources=SOURCES)


while True:
    try:
        loop()
    except Exception as e:
        raise e
        # TODO: log
        pass
    target = min([next_run_time(t) for t in REFRESH_TIMES])
    print('Sleeping until', target)
    sleep((target - get_now()).total_seconds())