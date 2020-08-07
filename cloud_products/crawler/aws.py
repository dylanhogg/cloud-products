import os
import logging
import collections
from crawler import base
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class AwsCrawler(base.Crawler):
    def __init__(self):
        self.base_url = "https://aws.amazon.com"
        self.seed_url = self.base_url + "/products/"

    def _parse_service(self, soup):
        tags = soup.find("main", attrs={"role": "main"})
        if tags is None:
            return []
        text = tags.text
        lines = text.splitlines()
        lines = list(l.strip() for l in lines if len(l.split()) > 0)
        return lines

    def _scrape_page(self, url, output_path, skip_cache):
        cache_filename = f"{output_path}{self.valid_filename(url)}.html"
        cache_filename_exists = Path(cache_filename).is_file()
        pickle_filename = cache_filename + ".pickle"
        loaded_from_cache = False

        os.makedirs(output_path, exist_ok=True)

        if skip_cache or not cache_filename_exists:
            logging.info(f"Scraping: {url}")
            response = urlopen(url)
            soup = BeautifulSoup(response, "html.parser")
            if cache_filename is not None:
                logging.info(f"Saving to cache: {cache_filename}")
                self.save(soup, cache_filename)
                self.pickle_dump(response, pickle_filename)
        else:
            logging.debug(f"Loading from cache: {cache_filename}")
            soup = self.load(cache_filename)
            response = self.pickle_load(pickle_filename)
            loaded_from_cache = True

        return response, soup, loaded_from_cache

    def get_child_pages(self, soup, base_url, seed_url):
        """
        Get child pages from seed url.
        """
        Service = collections.namedtuple(
            "Service", "name, std_name, rel_href, abs_href, base_url, seed_url, desc"
        )

        results = []
        tags = soup.find_all("div", attrs={"class": "lb-content-item"})

        # Example html snippet, 21 Feb 2019:
        # <div class="lb-content-item">
        # <a href="/cloudsearch/?c=1&amp;pt=2"> Amazon CloudSearch<span>Managed Search Service</span> </a>
        # </div>

        for tag in tags:
            a = tag.find("a")
            rel_href = a["href"]
            abs_href = base_url + rel_href
            # TODO: remove querystring from abs_href
            abs_href = urljoin(abs_href, urlparse(abs_href).path)
            name = a.contents[0].strip()
            std_name = name.lower().replace("amazon", "aws")
            desc = a.contents[1].text.strip()
            svc = Service(name, std_name, rel_href, abs_href, base_url, seed_url, desc)
            results.append(svc)

        return results

    def crawl_product(self, page, output_path, skip_cache):
        logging.info(
            f"Child: {page.std_name}, {page.name}, {page.desc}, {page.rel_href}"
        )
        url = page.abs_href
        logging.info(f"Url: {url}")
        (response, svc_soup, loaded_from_cache) = self._scrape_page(
            url, output_path, skip_cache
        )
        lines = self._parse_service(svc_soup)
        if len(lines) == 0:
            logging.warning(f"No matching lines for page: {page.std_name}")
            return []

        return lines

    def get_products(self, output_path, skip_cache=False):
        # Scrape seed index page
        (response, seed_soup, loaded_from_cache) = self._scrape_page(
            self.seed_url, output_path, skip_cache
        )

        # Parse service links from seed index page
        child_pages = self.get_child_pages(seed_soup, self.base_url, self.seed_url)

        return child_pages

    def get_product(self, page, output_path, skip_cache=False):
        logging.info(f"Crawling page: {page}")
        return self.crawl_product(page, output_path, skip_cache)
