import pathlib
import urllib
from .local_config import OUTPUT_PATH, PUBLIC_OUTPUT_PATH_BASE


def make_webcal_link(ics_url: str) -> str:
    return 'webcal://' + ics_url[len('https://'):]


def make_ical_link(ics_url: str) -> str:
    return make_webcal_link(ics_url)


def make_gcal_link(ics_url: str) -> str:
    """
    Convert a .ics URL to a Google Calendar subscription link.
    Replaces https:// with webcal:// and URL-encodes it.
    """
    encoded_url = urllib.parse.quote(make_webcal_link(ics_url), safe='')
    return f'https://calendar.google.com/calendar/r?cid={encoded_url}'


def make_html_row(source_name: str) -> str:
    ics_url = f'{PUBLIC_OUTPUT_PATH_BASE}{source_name}.ics'
    return (
        f'<li>'
        f'<a href="{make_ical_link(ics_url)}" class="external-link">iCal</a> | '
        f'<a href="{make_gcal_link(ics_url)}" class="external-link">Gcal</a> | '
        f'{source_name.replace("_", " ").title()}'
        f'</li>'
    )


def update_website():
    '''
    Updates the index.html file listing all available calendars.
    Errors are thrown and should be handled upstream.
    '''
    base_path = pathlib.Path(OUTPUT_PATH)
    index_path = base_path / 'index.html'
    template_path = pathlib.Path(__file__).parent / 'html_template.html'

    with open(template_path, 'r') as f:
        template_html = f.read()
    list_location = template_html.find('{calendars_list}')
    line_location = template_html[:list_location].rfind('\n')
    indentation = ' ' * (list_location - line_location - 1)

    calendars_list_items = []
    for file in base_path.iterdir():
        if file.suffix != '.ics':
            continue
        source_name = file.stem
        row = make_html_row(source_name)
        calendars_list_items.append(row if len(calendars_list_items) == 0 else indentation + row)
    calendars_list = '\n'.join(calendars_list_items)

    final_html = template_html.replace('{calendars_list}', calendars_list)

    with open(index_path, 'w') as f:
        f.write(final_html)