import logging
from crawler.aws import AwsCrawler


def run_crawler(crawler):
    products = AwsCrawler().get_products()

    for product in products:
        logging.info(f"{product.code}: {product.std_name}: {product.name}: {product.desc}")

    for product in products:
        logging.info(f"Crawling product: {product}")
        crawler.save_product(product, output_path)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    vendor = "aws"
    output_path = "./_data/scrape_results/"

    if vendor == "aws":
        run_crawler(AwsCrawler())

    elif vendor == "gcp":
        raise Exception(f"Google Cloud Compute not currently supported")

    elif vendor == "azure":
        raise Exception(f"Microsoft Azure not currently supported")

    else:
        raise Exception(f"Unknown vendor {vendor}")
