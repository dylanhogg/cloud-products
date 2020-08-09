import os
import string
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.default_cache_path = ".cloud-products-cache/"

    def valid_filename(self, url) -> str:
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = url.lower()
        filename = filename.replace("https://", "")
        filename = filename.replace("http://", "")
        filename = filename.replace("/", "_")
        filename = "".join(c for c in filename if c in valid_chars)
        filename = filename.replace(" ", "_")
        return filename

    def load(self, filename) -> BeautifulSoup:
        html = open(filename).read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def save(self, obj, filename) -> None:
        with open(filename, "w") as f:
            f.write(str(obj))

    def save_product(self, product, output_path, cache_path=None, use_cache=True) -> None:
        if cache_path is None:
            cache_path = self.default_cache_path

        lines = self.get_product_text(product, cache_path, use_cache)
        text = "\n".join(lines)
        url = product.abs_href
        filename = f"{output_path}/{self.valid_filename(url)}_content.txt"

        os.makedirs(output_path, exist_ok=True)
        self.save(text, filename)
