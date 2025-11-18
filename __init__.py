from .fetch import fetch_and_save_events
from .local_config import BASE_SOURCES
from .website import update_website

for source in BASE_SOURCES:
    fetch_and_save_events(source=source)
update_website()