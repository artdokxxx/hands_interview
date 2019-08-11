import logging

from phones_scraper.common.state import StateManager
from phones_scraper.common.scraper import ScraperManager
from phones_scraper.sites import get_sites

logging.basicConfig(level=logging.WARN)
scraper_manager = ScraperManager(get_sites())
state_manager = StateManager()

res = scraper_manager.run()

for r in res:
    print(f'[{r[0].main}] founded {len(r[1])} phones: {r[1]}')

state_manager.reset_state()
