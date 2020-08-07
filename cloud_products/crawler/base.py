import string
import pickle
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        pass

    def valid_filename(self, url):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = url.replace("/", "_")
        filename = "".join(c for c in filename if c in valid_chars)
        filename = filename.replace(" ", "_")
        return filename

    def pickle_dump(self, obj, filename):
        with open(filename, "wb") as handle:
            pickle.dump(obj, handle)

    def pickle_load(self, filename):
        with open(filename, "rb") as handle:
            return pickle.load(handle)

    def load(self, filename):
        html = open(filename).read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def save(self, obj, filename):
        with open(filename, "w") as f:
            f.write(str(obj))

    def save_product(self, product, output_path, skip_cache=False):
        lines = self.get_product(product, output_path, skip_cache)
        text = "\n".join(lines)
        url = product.abs_href
        filename = f"{output_path}/{self.valid_filename(url)}_content.txt"
        self.save(text, filename)
