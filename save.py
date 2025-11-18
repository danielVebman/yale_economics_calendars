from datetime import datetime
from icalendar import Calendar, Event
import pandas as pd
from pathlib import Path

from .local_config import PRIVATE_OUTPUT_PATH
from .source import Source


def save_events(*, source: Source, events: pd.DataFrame) -> Path:
    '''
    Saves the events DataFrame into ICS files named after the source ID.
    Errors are thrown and should be handled upstream.
    '''
    base_path = Path(PRIVATE_OUTPUT_PATH)
    base_path.mkdir(parents=False, exist_ok=True)
    ics_path = base_path / (source.id + '.ics')
    save_events_to_ics(source=source, events=events, file_path=ics_path)
    return ics_path


def save_events_to_ics(*, source: Source, events: pd.DataFrame, file_path: str) -> None:
    """
    Saves the events DataFrame to an ICS file at the specified file path.
    Errors are thrown and should be handled upstream.
    """
    cal = Calendar()
    cal.add('prodid', '-//Daniel Vebman - danielvebman.com//')
    cal.add('version', '2.0')
    cal.add('method', 'PUBLISH')
    cal.add('X-WR-CALNAME', source.name)
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
