from .fetch import fetch_and_save_events
from .local_config import ECONOMETRICS_PROSPECTUS_LUNCH_SOURCE

# if __name__ == '__main__':
fetch_and_save_events(source=ECONOMETRICS_PROSPECTUS_LUNCH_SOURCE)