import os
import logging
from cloud_products import base
from cloud_products.product import Product
from pathlib import Path
from typing import List, Tuple
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class AwsCrawler(base.Crawler):
    def __init__(self):
        self.base_url = "https://aws.amazon.com"
        self.seed_url = self.base_url + "/products/"
        super(AwsCrawler, self).__init__()

    @staticmethod
    def _parse_product(soup) -> List[str]:
        tags = soup.find("main", attrs={"role": "main"})
        if tags is None:
            return []
        text = tags.text
        lines = text.splitlines()
        lines = list(l.strip() for l in lines if len(l.split()) > 0)
        return lines

    def _scrape_page(self, url, cache_path, use_cache) -> Tuple[BeautifulSoup, bool]:
        cache_filename = f"{cache_path}aws-{self.valid_filename(url)}.html"
        cache_filename_exists = Path(cache_filename).is_file()
        loaded_from_cache = False

        logging.debug(f"use_cache = {use_cache}")
        logging.debug(f"cache_filename = {cache_filename}")
        os.makedirs(cache_path, exist_ok=True)

        if not use_cache or not cache_filename_exists:
            logging.debug(f"Scraping: {url}")
            response = urlopen(url)
            soup = BeautifulSoup(response, "html.parser")
            if cache_filename is not None:
                logging.debug(f"Saving to cache: {cache_filename}")
                self.save(soup, cache_filename)
        else:
            logging.debug(f"Loading from cache: {cache_filename}")
            soup = self.load(cache_filename)
            loaded_from_cache = True

        return soup, loaded_from_cache

    @staticmethod
    def _get_child_pages(soup, base_url, seed_url) -> List[Product]:
        """
        Get child pages from seed url.
        """
        results = []
        tags = soup.find_all("div", attrs={"class": "lb-content-item"})

        # Example html snippet, 21 Feb 2019:
        # <div class="lb-content-item">
        # <a href="/cloudsearch/?c=1&amp;pt=2"> Amazon CloudSearch<span>Managed Search Service</span> </a>
        # </div>

        crawled = []
        for tag in tags:
            a = tag.find("a")
            if a["href"].startswith("http"):
                # Ignore beta products linking to external addresses
                continue

            rel_href = urlparse(a["href"]).path
            abs_href = urljoin(base_url, rel_href)
            code = rel_href.replace("/", "").strip().lower()
            name = a.contents[0].strip()
            std_name = name.lower().replace("amazon", "aws")
            desc = a.contents[1].text.strip()
            product = Product(name, std_name, code, rel_href, abs_href, base_url, seed_url, desc)

            if std_name in crawled:
                # Duplicate links can exist in page, skip these
                continue

            crawled.append(std_name)
            results.append(product)

        return results

    def _crawl_product_text(self, page, cache_path, use_cache) -> List[str]:
        logging.debug(f"Child: {page.std_name}, {page.name}, {page.desc}, {page.rel_href}")
        url = page.abs_href
        logging.debug(f"Url: {url}")
        (svc_soup, loaded_from_cache) = self._scrape_page(url, cache_path, use_cache)
        lines = self._parse_product(svc_soup)
        if len(lines) == 0:
            logging.warning(f"No matching lines for page: {page.std_name}")
            return []

        return lines

    def get_products(self, cache_path=None, use_cache=True) -> List[Product]:
        if cache_path is None:
            cache_path = self.default_cache_path

        # Scrape seed index page
        (seed_soup, loaded_from_cache) = self._scrape_page(self.seed_url, cache_path, use_cache)

        # Parse product links from seed index page
        child_pages = self._get_child_pages(seed_soup, self.base_url, self.seed_url)

        return sorted(child_pages)

    def get_products_matching(self, match, cache_path=None, use_cache=True) -> List[Product]:
        products = self.get_products(cache_path, use_cache)
        return [p for p in products if match.lower() in p.name.lower()]

    def get_product_text(self, page, cache_path=None, use_cache=True) -> List[str]:
        if cache_path is None:
            cache_path = self.default_cache_path

        logging.debug(f"Crawling page: {page}")
        return self._crawl_product_text(page, cache_path, use_cache)
