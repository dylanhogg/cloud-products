import os
import shutil
from crawler import aws

cache_path = "./_data/test_cache_path/"
output_path = "./_data/test_output_path/"


def remove_dirs():
    if os.path.exists(cache_path) and os.path.isdir(cache_path):
        shutil.rmtree(cache_path)
    if os.path.exists(output_path) and os.path.isdir(output_path):
        shutil.rmtree(output_path)


def test_aws_get_products_has_good_rel_href():
    remove_dirs()
    crawler = aws.AwsCrawler()

    products = crawler.get_products()
    assert(len([p for p in products if p.rel_href.strip() == "/"]) == 0)
    assert(len([p for p in products if "?" in p.rel_href]) == 0)


def test_aws_get_products_matching():
    remove_dirs()
    crawler = aws.AwsCrawler()

    products = crawler.get_products_matching("aws glue")
    assert(len(products) == 1)
    assert(products[0].name == "AWS Glue")
    assert(products[0].std_name == "aws glue")
    assert(products[0].code == "glue")

    lines = crawler.get_product_text(products[0])
    assert len(lines) > 0


def test_aws_crawl_lines():
    remove_dirs()
    crawler = aws.AwsCrawler()

    products = crawler.get_products()
    for product in products[:3]:
        lines = crawler.get_product_text(product)
        assert len(lines) > 0


def test_aws_crawl_save_product():
    remove_dirs()
    crawler = aws.AwsCrawler()

    products = crawler.get_products()
    for product in products[:3]:
        crawler.save_product(product, output_path)


def test_aws_crawl_cached_lines():
    remove_dirs()
    use_cache = True
    crawler = aws.AwsCrawler()

    # Prime cache
    products = crawler.get_products(cache_path, use_cache)
    for product in products[:3]:
        lines = crawler.get_product_text(product, cache_path, use_cache)
        assert len(lines) > 0

    products = crawler.get_products(cache_path, use_cache)
    for product in products[:3]:
        lines = crawler.get_product_text(product, cache_path, use_cache)
        assert len(lines) > 0


def test_aws_crawl_cached_save_product():
    remove_dirs()
    use_cache = True
    crawler = aws.AwsCrawler()

    # Prime cache
    products = crawler.get_products(cache_path, use_cache)
    for product in products[:3]:
        crawler.save_product(product, output_path, cache_path, use_cache)

    products = crawler.get_products(cache_path, use_cache)
    for product in products[:3]:
        crawler.save_product(product, output_path, cache_path, use_cache)


def test_aws_crawl_nocache_lines():
    remove_dirs()
    use_cache = False
    crawler = aws.AwsCrawler()

    products = crawler.get_products(cache_path, use_cache)
    for product in products[:3]:
        lines = crawler.get_product_text(product, cache_path, use_cache)
        assert len(lines) > 0


def test_aws_crawl_nocache_save_product():
    remove_dirs()
    use_cache = False
    crawler = aws.AwsCrawler()

    products = crawler.get_products(cache_path, use_cache)
    for product in products[:3]:
        crawler.save_product(product, output_path, cache_path, use_cache)
