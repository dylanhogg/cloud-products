import os
import logging
import re
import unicodedata
from cloud_products import base
from cloud_products.product import Product
from pathlib import Path
from typing import List, Tuple
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.firefox.options import Options


class Browser(base.Crawler):
    def get_page_source(self, page: int) -> List[Product]:
        # TODO: add caching
        assert isinstance(page, int), "page must be an integer"

        options = Options()
        options.add_argument("--headless")

        url_format = ("https://aws.amazon.com/products/" 
                              "?aws-products-all.sort-by=item.additionalFields.productNameLowercase" 
                              "&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=*all&awsf.tech-category=*all" 
                              "&awsm.page-aws-products-all={page}")
        url_page = url_format.format(page=page)

        # {"message":"API rate limit exceeded for 101.184.146.239. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)","documentation_url":"https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"}
        driver = webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))
        driver.set_window_size(1120, 550)
        driver.maximize_window()
    
        driver.get(url_page)
        wait = WebDriverWait(driver, 40)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".m-card-main")))  # TODO: review class m-card-main
        source = driver.page_source

        driver.quit()  # TODO: reuse driver for other pages

        return source
