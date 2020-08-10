import os
import string
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.default_cache_path = ".cloud-products-cache/"

    @staticmethod
    def valid_filename(url) -> str:
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = url.lower()
        filename = filename.replace("https://", "")
        filename = filename.replace("http://", "")
        filename = filename.replace("/", "_")
        filename = "".join(c for c in filename if c in valid_chars)
        filename = filename.replace(" ", "_")
        return filename

    @staticmethod
    def load(filename) -> BeautifulSoup:
        html = open(filename).read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @staticmethod
    def save(obj, filename) -> None:
        with open(filename, "w") as f:
            f.write(str(obj))

    def save_product(self, product, output_path, output_filename=None, cache_path=None, use_cache=True) -> str:
        if cache_path is None:
            cache_path = self.default_cache_path

        lines = self.get_product_text(product, cache_path, use_cache)
        text = "\n".join(lines)
        url = product.abs_href

        if output_filename is None:
            filename = os.path.join(output_path, f"{self.valid_filename(url)}_content.txt")
        else:
            filename = os.path.join(output_path, output_filename)

        os.makedirs(output_path, exist_ok=True)
        self.save(text, filename)
        return filename
