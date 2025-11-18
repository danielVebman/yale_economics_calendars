import requests
from pathlib import Path
from .parse import extract_events
from .save import save_events
from .source import Source


def fetch_and_save_events(*, source: Source) -> Path:
    '''
    Fetches events from `source`, parses them, and saves into a DataFrame.
    Returns the path where the ics file was saved.
    Errors are thrown and should be handled upstream.
    '''
    response = requests.get(source.url, timeout=15)
    response.raise_for_status()
    events = extract_events(response.text)
    save_events(source=source, events=events)