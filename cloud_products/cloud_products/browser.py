from cloud_products import base
from cloud_products.product import Product
from typing import List

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.firefox.options import Options

_options = Options()
_options.add_argument("--headless")
_driver = webdriver.Firefox(options=_options, service=Service(GeckoDriverManager().install()))


class Browser(base.Crawler):
    def get_page_source(self, page: int) -> List[Product]:
        # TODO: add caching
        assert isinstance(page, int), "page must be an integer"
        assert page > 0, "page must be greater than 0"

        url_format = (
            "https://aws.amazon.com/products/"
            "?aws-products-all.sort-by=item.additionalFields.productNameLowercase"
            "&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=*all&awsf.tech-category=*all"
            "&awsm.page-aws-products-all={page}"
        )
        url_page = url_format.format(page=page)

        _driver.set_window_size(1120, 550)
        _driver.maximize_window()
        _driver.get(url_page)
        wait = WebDriverWait(_driver, 40)
        wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".m-card-main"))
        )  # TODO: review class m-card-main
        source = _driver.page_source
        return source

    def quit(self):
        _driver.quit()
