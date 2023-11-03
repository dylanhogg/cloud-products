import os
import logging
import re
import unicodedata
from cloud_products import base
from cloud_products.browser import Browser
from cloud_products.product import Product
from pathlib import Path
from typing import List, Tuple
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class AwsCrawler(base.Crawler):
    def __init__(self):
        self.base_url = "https://aws.amazon.com"
        #self.seed_url = self.base_url + "/products/"
        # self.seed_url = self.base_url + "/products/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=*all&awsf.tech-category=*all"
        # self.seed_url = self.base_url + "/products/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=*all&awsf.tech-category=*all&awsm.page-aws-products-all=2"
        super(AwsCrawler, self).__init__()

    @staticmethod
    def normalise_chars(line, remove_chars) -> str:
        new_line = line
        new_line = unicodedata.normalize("NFKD", new_line)  # Normalise &nbsp etc.
        new_line = re.sub(r"^Q\.", "Q:", new_line.strip())  # Some AWS faq pages are inconsistent with Qn prefix.
        new_line = re.sub(r"^Q\:[ ]+", "Q: ", new_line.strip())  # Normalise spacing.
        new_line = re.sub(r">>$", "", new_line.strip())  # Remove trailing >>
        new_line = new_line.translate({ord(i): None for i in remove_chars})  # Remove chars using translate().
        return new_line.strip()

    @staticmethod
    def _parse_product(soup, min_line_length=1, remove_chars=None) -> List[str]:
        if remove_chars is None:
            remove_chars = ["»", "\n", "\r"]

        tags = soup.find("main", attrs={"role": "main"})
        if tags is None:
            return []

        text = tags.text
        lines = text.splitlines()
        lines = list(
            AwsCrawler.normalise_chars(line, remove_chars) for line in lines if len(line.split()) >= min_line_length
        )
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
        tags = soup.find_all("div", attrs={"class": "m-card-container"})

        # Example html snippet, 21 Feb 2019:
        # <div class="lb-content-item">
        # <a href="/cloudsearch/?c=1&amp;pt=2"> Amazon CloudSearch<span>Managed Search Service</span> </a>
        # </div>

        crawled = []
        for tag in tags:
            a = tag.find("a")
            # if a["href"].startswith("http"):
            #     # Ignore beta products linking to external addresses
            #     # 2022: all start with http??
            #     continue

            rel_href = urlparse(a["href"]).path
            abs_href = urljoin(base_url, rel_href)
            abs_href_faq = urljoin(base_url, rel_href + "faqs/")
            code = rel_href.replace("/", "").strip().lower()
            name = a.find("div", attrs={"class": "m-headline"}).text.strip()
            std_name = name.lower().replace("amazon", "aws")
            desc = a.find("div", attrs={"class": "m-desc"}).text.strip()
            # category = a.find("div", attrs={"class": "m-category"}).text.strip()  # TODO: new
            # flag = a.find("div", attrs={"class": "m-flag"}).text.strip()  # TODO: new
            product = Product(name, std_name, code, rel_href, abs_href, abs_href_faq, base_url, seed_url, desc)

            if std_name in crawled:
                # Duplicate links can exist in page, skip these
                continue

            crawled.append(std_name)
            results.append(product)

        return results

    def _crawl_product_text(self, page, cache_path, use_cache, dedupe=True) -> List[str]:
        logging.debug(f"Child: {page.std_name}, {page.name}, {page.desc}, {page.rel_href}")
        url = page.abs_href
        logging.debug(f"Url: {url}")
        (svc_soup, loaded_from_cache) = self._scrape_page(url, cache_path, use_cache)
        lines = self._parse_product(svc_soup)

        if len(lines) == 0:
            logging.warning(f"No matching lines for product page: {page.std_name}")
            return []

        return self.dedupe_list(lines) if dedupe else lines

    def _crawl_faq_text(self, page, cache_path, use_cache, dedupe=True) -> List[str]:
        logging.debug(f"Child: {page.std_name}, {page.name}, {page.desc}, {page.rel_href}")
        url = page.abs_href_faq
        logging.debug(f"Url: {url}")
        (svc_soup, loaded_from_cache) = self._scrape_page(url, cache_path, use_cache)
        lines = self._parse_product(svc_soup)

        if len(lines) == 0:
            logging.warning(f"No matching lines for faq page: {page.std_name}")
            return []

        return self.dedupe_list(lines) if dedupe else lines

    def get_products(self, page: int, cache_path=None, use_cache=True) -> List[Product]:
        if cache_path is None:
            cache_path = self.default_cache_path

        assert isinstance(page, int), "page must be an integer"

        seed_url_formatter = ("https://aws.amazon.com/products/" 
                              "?aws-products-all.sort-by=item.additionalFields.productNameLowercase" 
                              "&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=*all&awsf.tech-category=*all" 
                              "&awsm.page-aws-products-all={page}")
        override_seed_url = seed_url_formatter.format(page=page)

        browser = Browser()
        source = browser.get_page_source(page)
        seed_soup = BeautifulSoup(source, "html.parser")
        # print(seed_soup)

        # Parse product links from seed index page
        child_pages = self._get_child_pages(seed_soup, self.base_url, override_seed_url)
        return sorted(child_pages)

    def get_products_as_df(self, cache_path=None, use_cache=True):
        try:
            # NOTE: pandas is a soft requirement for this package.
            #       This method will fail if pandas isn't installed.
            import pandas as pd
        except ModuleNotFoundError:
            raise ModuleNotFoundError("pandas must be installed to use this method. Try `pip install pandas`.")

        products = self.get_products(cache_path=cache_path, use_cache=use_cache)
        product_text = {}
        for product in products:
            product_lines = self.get_product_text(product, use_cache=use_cache)
            product_text[product.code] = " ".join(product_lines)
        df = pd.DataFrame.from_records([vars(p) for p in products])
        df["product_text"] = df["code"].apply(lambda code: product_text[code])
        return df

    def get_products_matching(self, match, cache_path=None, use_cache=True) -> List[Product]:
        products = self.get_products(cache_path, use_cache)
        return [p for p in products if match.lower() in p.name.lower()]

    def get_product_text(self, page, cache_path=None, use_cache=True) -> List[str]:
        if cache_path is None:
            cache_path = self.default_cache_path

        logging.debug(f"Crawling product page: {page}")
        return self._crawl_product_text(page, cache_path, use_cache)

    def get_faq_text(self, page, cache_path=None, use_cache=True) -> List[str]:
        if cache_path is None:
            cache_path = self.default_cache_path

        logging.debug(f"Crawling faq page: {page}")
        try:
            return self._crawl_faq_text(page, cache_path, use_cache)
        except HTTPError as err:
            if err.code == 404:
                # TODO: get real faq link from page.abs_href and propagate this back to caller.
                #       E.g. https://aws.amazon.com/elastic-inference/ points to
                #       https://aws.amazon.com/machine-learning/elastic-inference/
                #       E.g. https://aws.amazon.com/rds/aurora/serverless/ links to parent page.
                if "/faqs/" in page.abs_href_faq:
                    # HACK: Fix AWS products that have an inconsistent faq url.
                    page.abs_href_faq = page.abs_href_faq.replace("/faqs", "/faq")
                    logging.debug(
                        f"FAQ page did not exist for {page.code}. Trying new abs_href_faq: {page.abs_href_faq}"
                    )
                    return self.get_faq_text(page, cache_path, use_cache)
                else:
                    logging.warning(f"FAQ page did not exist for page (or alternatives): {page.abs_href_faq}")
                    return None
            else:
                raise err
