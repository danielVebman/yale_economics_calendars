from pathlib import Path
import typing as T

from .local_config import PRIVATE_OUTPUT_PATH, PUBLIC_OUTPUT_PATH
from .source import Source
from .utils import get_now


def make_webcal_link(ics_url: str) -> str:
    return 'webcal://' + ics_url[len('https://'):]


def make_ical_link(ics_url: str) -> str:
    return make_webcal_link(ics_url)


def make_gcal_link(ics_url: str) -> str:
    return f'https://calendar.google.com/calendar/r?cid={make_webcal_link(ics_url)}'


def make_html_row(*, source: Source) -> str:
    ics_url = f'{PUBLIC_OUTPUT_PATH}{source.id}.ics'
    return (
        f'<li class="icon-row">'
        f'<a class="icon-circle-link" aria-label="Apple Calendar" href="{make_ical_link(ics_url)}"><img src="/icons/apple.svg" alt="iCal"/></a>'
        f'<a class="icon-circle-link" aria-label="Google Calendar" href="{make_gcal_link(ics_url)}"><img src="/icons/gcal.svg" alt="Gcal"/></a>'
        f'<a class="icon-circle-link copy-link-btn" aria-label="WebCal ICS URL" href="{make_webcal_link(ics_url)}"><img src="/icons/link.svg" alt="WebCal ICS URL"/></a>'
        f'<a href="{source.url}" class="external-link" style="padding-left: 10px">{source.name}</a>'
        f'</li>'
    )


def update_website(sources: T.List[Source]) -> None:
    '''
    Updates the index.html file listing the `sources`.
    Errors are thrown and should be handled upstream.
    '''
    index_path = Path(PRIVATE_OUTPUT_PATH) / 'index.html'
    template_path = Path(__file__).parent / 'html_template.html'

    with open(template_path, 'r') as f:
        template_html = f.read()
    list_location = template_html.find('{calendars_list}')
    line_location = template_html[:list_location].rfind('\n')
    indentation = ' ' * (list_location - line_location - 1)

    calendars_list_items = []
    for source in sources:
        row = make_html_row(source=source)
        calendars_list_items.append(row if len(calendars_list_items) == 0 else indentation + row)
    calendars_list = '\n'.join(calendars_list_items)

    now = get_now().strftime('%Y-%m-%d %H:%M:%S')
    final_html = (
        template_html
            .replace('{update_datetime}', now)
            .replace('{calendars_list}', calendars_list)
    )

    with open(index_path, 'w') as f:
        f.write(final_html)