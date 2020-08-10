import logging


def run_aws_crawler():
    logging.info("Example 1: List AWS products")
    from crawler.aws import AwsCrawler
    for product in AwsCrawler().get_products():
        print(f"{product.code}: {product.name}: {product.desc}")

    logging.info("Example 2: Get product descriptions as a list of lines")
    from crawler.aws import AwsCrawler
    crawler = AwsCrawler()
    product = crawler.get_products()[0]
    lines = crawler.get_product_text(product)
    print(lines[4])

    logging.info("Example 3: Get matching product(s)")
    from crawler.aws import AwsCrawler
    crawler = AwsCrawler()
    sagemaker_products = crawler.get_products_matching("sagemaker")
    sagemaker_description = crawler.get_product_text(sagemaker_products[0])
    print(sagemaker_description[3])

    logging.info("Example 4: Save product descriptions to files:")
    from crawler.aws import AwsCrawler
    for product in AwsCrawler().get_products():
        print(f"Saving {product.name}")
        crawler.save_product(product, output_path)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    vendor = "aws"
    output_path = "./_data/scrape_results/"

    if vendor == "aws":
        run_aws_crawler()

    elif vendor == "gcp":
        raise Exception(f"Google Cloud Compute not currently supported")

    elif vendor == "azure":
        raise Exception(f"Microsoft Azure not currently supported")

    else:
        raise Exception(f"Unknown vendor {vendor}")
