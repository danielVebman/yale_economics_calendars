from ics import Calendar, Event
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
    csv_path = base_path / (source.name + '.csv')
    ics_path = base_path / (source.name + '.ics')
    save_events_to_csv(events=events, file_path=csv_path)
    save_events_to_ics(events=events, file_path=ics_path)


def save_events_to_csv(events: pd.DataFrame, file_path: str) -> None:
    '''
    Saves the events DataFrame to a CSV file at the specified file path.
    Errors are thrown and should be handled upstream.
    '''
    events.to_csv(file_path, index=False)


def save_events_to_ics(events: pd.DataFrame, file_path: str) -> None:
    '''
    Saves the events DataFrame to an ICS file at the specified file path.
    Errors are thrown and should be handled upstream.
    '''
    calendar = Calendar()

    for _, data in events.iterrows():
        if pd.isna(data['date']) or pd.isna(data['start_time']) or pd.isna(data['end_time']):
            # TODO: log
            continue
        event = Event()
        event.name = data['title']
        event.begin = f'{data["date"]} {data["start_time"]}'
        event.end = f'{data["date"]} {data["end_time"]}'
        event.location = data['location'] if pd.notna(data['location']) else ''
        event.description = f'Paper URL: {data["paper_url"]}\nOther Info: {data["other_info"]}'
        calendar.events.add(event)

    with open(file_path, 'w') as f:
        f.writelines(calendar)