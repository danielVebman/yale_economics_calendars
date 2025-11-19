from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import regex as re

from .utils import ET


def extract_events(html_content: str) -> pd.DataFrame:
    '''
    Parses the HTML content to extract event data into a pandas DataFrame.
    Errors are thrown and should be handled upstream.
    '''
    soup = BeautifulSoup(html_content, 'html.parser')
    event_data = []

    for article in soup.find_all('article', class_='node-teaser--event'):
        data = {
            'series': None,
            'date': None,
            'title': None,
            'event_url': None,
            'start_datetime': None,
            'end_datetime': None,
            'location': None,
            'paper_url': None,
            'other_info': None
        }

        # Extract series
        if series_tag := article.find('div', class_='node-teaser__event-series'):
             if series_name := series_tag.get_text(strip=True):
                 data['series'] = series_name

        # Extract date
        if date_block := article.find('div', class_='node-teaser__event-start-date'):
            date_parts = date_block.get_text(separator=' ', strip=True)
            data['date'] = dt.datetime.strptime(date_parts, '%b %d %Y').date()

        # Extract title
        if title_tag := article.select_one('.node-teaser__heading a span'):
            data['title'] = title_tag.get_text(strip=True)
        
        # Extract event url
        if event_url_tag := article.select_one('.node-teaser__heading a'):
            if 'href' in event_url_tag.attrs:
                data['event_url'] = event_url_tag['href']
                if data['event_url'].startswith('/'):
                    data['event_url'] = 'https://economics.yale.edu' + data['event_url']

        # Extract time
        if time_tag := article.find('div', class_='node-teaser__event-date-additional'):
            time_text = time_tag.get_text(strip=True).replace('Time:', '').strip()
            data['start_datetime'], data['end_datetime'] = [
                dt.datetime.combine(
                    data['date'], 
                    dt.datetime.strptime(p.strip(), '%I:%M %p').time()
                ).replace(tzinfo=ET)
                for p in time_text.split('—')
            ]

        # Extract location
        if location_tag := article.find('div', class_='node-teaser__address-label'):
            data['location'] = location_tag.get_text(strip=True)

        # Extract paper URL
        if paper_url_tag := article.find('div', class_='node-teaser__event-paper'):
            link = paper_url_tag.find('a')
            if link and 'href' in link.attrs:
                data['paper_url'] = link['href']
                if data['paper_url'].startswith('/'):
                    data['paper_url'] = 'https://economics.yale.edu' + data['paper_url']

        # Extract other info (notes and joint authors)
        other_info_list = []
        
        if notes_tag := article.find('div', class_='node-teaser__notes'):
            notes = notes_tag.get_text(strip=True)
            if notes:
                other_info_list.append(notes)

        if authors_tag := article.find('div', class_='node-teaser__joint-authors'):
            authors = authors_tag.get_text(strip=True)
            if authors_clean := re.sub(r'Joint with:\s*', '', authors, flags=re.IGNORECASE).strip():
                other_info_list.append(f'Joint with: {authors_clean}')

        if len(other_info_list) > 0:
             data['other_info'] = ' | '.join(other_info_list)

        event_data.append(data)

    return pd.DataFrame(event_data)