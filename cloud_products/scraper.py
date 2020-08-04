import logging
from crawler import aws

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    vendor = "aws"

    output_path = "./_data/scrape_results/"
    skip_cache = False

    if vendor == "aws":
        crawler = aws.AwsCrawler()
        products = crawler.get_products(output_path, skip_cache)
        for product in products:
            crawler.save_product(product, output_path, skip_cache)

    elif vendor == "gcp":
        raise Exception(f"Google Cloud Compute not currently supported")

    elif vendor == "azure":
        raise Exception(f"Microsoft Azure not currently supported")

    else:
        raise Exception(f"Unknown vendor {vendor}")
