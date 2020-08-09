import logging
from crawler import aws

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    vendor = "aws"
    output_path = "./_data/scrape_results/"

    if vendor == "aws":
        crawler = aws.AwsCrawler()
        for product in crawler.get_products():
            logging.info(f"Crawling product: {product}")
            crawler.save_product(product, output_path)

    elif vendor == "gcp":
        raise Exception(f"Google Cloud Compute not currently supported")

    elif vendor == "azure":
        raise Exception(f"Microsoft Azure not currently supported")

    else:
        raise Exception(f"Unknown vendor {vendor}")
