import time
import re
import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
from concurrent.futures import ALL_COMPLETED

from phones_scraper.config import get_config
from phones_scraper.common.state import StateManager


class ScraperManager(object):

    def __init__(self, sites):
        self.state_manager = StateManager()
        self.sites = sites
        self.config = get_config()
        self.timeout = getattr(self.config, 'TIMEOUT', 10)
        self.re_rule = getattr(self.config, 'RE_RULE', False)
        self.default_area_code = getattr(self.config, 'DEFAULT_AREA_CODE')

        logging.info(f'Scraper init - timeout: {self.timeout}')
        logging.info(f'Scraper init - sites: {self.sites}')

    def parse_phones(self, text):
        res = []
        if not self.re_rule:
            logging.warning('Regexp rule for parsing phones isn\'t defined.')
            raise Exception('Regexp rule for parsing phones isn\'t defined.')

        # Remove all styles and scripts
        soup = BeautifulSoup(text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()

        phones = re.findall(self.re_rule, soup.get_text())
        for r in phones:
            r = "".join(filter(str.isdigit, r))

            if not r or len(r) < 7:
                continue

            if len(r) == 7:
                r = f'{self.default_area_code}{r}'

            res.append(f'8{r}')

        return res

    async def __fetch_phones(self, site):
        logging.info(f'Start fetch phones in {site.main}')

        if self.state_manager.check_state(site.id):
            logging.info(f'Return fetch phones from state cache - {site.main}')
            return self.state_manager.get_state(site.id)

        start = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url=site.page_contacts)
        except:  # TODO except only some situation, not all
            return []

        status = response.status
        if status != 200:
            return []

        response = await response.text()
        phones = self.parse_phones(response)

        self.state_manager.save_state(site.id, phones)
        logging.info(f'{site.main} is done, took:{time.time() - start}')
        return site, phones

    async def get_future(self):
        res = []
        futures = [self.__fetch_phones(site) for site in self.sites]
        done, pending = await asyncio.wait(
            futures,
            timeout=self.timeout,
            return_when=ALL_COMPLETED
        )

        for future in pending:
            future.cancel()

        for future in done:
            r_ = future.result()
            if r_:
                res.append(future.result())

        return res

    def run(self):
        ev_loop = asyncio.get_event_loop()
        res = ev_loop.run_until_complete(self.get_future())
        ev_loop.close()

        return res
