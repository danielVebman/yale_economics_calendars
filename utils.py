import datetime as dt
from zoneinfo import ZoneInfo


get_now = lambda: dt.datetime.now(ZoneInfo("America/New_York"))
