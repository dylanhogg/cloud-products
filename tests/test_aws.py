import os
import shutil
from crawler import aws

output_path = "./_data/test_aws/"


def remove_dir(dirpath):
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(output_path)


def test_aws_crawl_cached_lines():
    remove_dir(output_path)
    skip_cache = False
    crawler = aws.AwsCrawler()
    products = crawler.get_products(output_path, skip_cache)

    for product in products[:3]:
        lines = crawler.get_product(product, output_path, skip_cache)
        assert len(lines) > 0


def test_aws_crawl_cached_save_product():
    remove_dir(output_path)
    skip_cache = False
    crawler = aws.AwsCrawler()
    products = crawler.get_products(output_path, skip_cache)

    for product in products[:3]:
        crawler.save_product(product, output_path, skip_cache)


def test_aws_crawl_nocache_lines():
    remove_dir(output_path)
    skip_cache = True
    crawler = aws.AwsCrawler()
    products = crawler.get_products(output_path, skip_cache)

    for product in products[:3]:
        lines = crawler.get_product(product, output_path, skip_cache)
        assert len(lines) > 0


def test_aws_crawl_nocache_save_product():
    remove_dir(output_path)
    skip_cache = True
    crawler = aws.AwsCrawler()
    products = crawler.get_products(output_path, skip_cache)

    for product in products[:3]:
        crawler.save_product(product, output_path, skip_cache)
