from datetime import datetime
from icalendar import Calendar, Event
import pandas as pd
import pathlib

from .local_config import OUTPUT_PATH
from .source import Source


def save_events(*, source: Source, events: pd.DataFrame):
    '''
    Saves the events DataFrame into CSV and ICS files named after the source.
    Errors are thrown and should be handled upstream.
    '''
    base_path = pathlib.Path(OUTPUT_PATH)
    base_path.mkdir(parents=False, exist_ok=True)
    # csv_path = base_path / (source.name + '.csv')
    ics_path = base_path / (source.name + '.ics')
    # save_events_to_csv(events=events, file_path=csv_path)
    save_events_to_ics(events=events, file_path=ics_path)


def save_events_to_csv(events: pd.DataFrame, file_path: str) -> None:
    '''
    Saves the events DataFrame to a CSV file at the specified file path.
    Errors are thrown and should be handled upstream.
    '''
    events.to_csv(file_path, index=False)


from icalendar import Calendar, Event
from datetime import datetime
import pandas as pd

def save_events_to_ics(events: pd.DataFrame, file_path: str) -> None:
    """
    Saves the events DataFrame to an ICS file at the specified file path.
    Errors are thrown and should be handled upstream.
    """
    cal = Calendar()
    cal.add('prodid', '-//Daniel Vebman - danielvebman.com//')
    cal.add('version', '2.0')
    cal.add('method', 'PUBLISH')
    cal.add('X-WR-CALNAME', file_path.stem.replace('_', ' ').title())
    cal.add('X-PUBLISHED-TTL', 'PT1H')

    for _, data in events.iterrows():
        if pd.isna(data['start_datetime']) or pd.isna(data['end_datetime']):
            continue

        evt = Event()
        evt.add('summary', data['title'])
        evt.add('dtstart', pd.to_datetime(data['start_datetime']).to_pydatetime())
        evt.add('dtend', pd.to_datetime(data['end_datetime']).to_pydatetime())

        if pd.notna(data['location']):
            evt.add('location', data['location'])

        description_parts = {
            'event_url': 'Event URL',
            'paper_url': 'Paper URL',
            'other_info': 'Other Info'
        }
        description_lines = []
        for key, label in description_parts.items():
            if pd.notna(data[key]):
                description_lines.append(f'{label}: {data[key]}')
        if description_lines:
            evt.add('description', '\n'.join(description_lines))

        cal.add_component(evt)

    with open(file_path, 'wb') as f:
        f.write(cal.to_ical())
