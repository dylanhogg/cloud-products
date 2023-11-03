import logging


def run_full_aws_crawler():
    logging.info("Run full AWS Crawler and save to files:")
    from cloud_products.aws import AwsCrawler

    crawler = AwsCrawler()
    all_products = []

    page_count = 17  # TODO: get count from page
    # page_count = 1  # Testing
    for page in range(1, page_count + 1):
        page_products = crawler.get_products(page=page)
        all_products.extend(page_products)
        print(f"Found {len(page_products)} products on page {page}...")
    print(f"Found {len(all_products)} TOTAL products.")

    for product in all_products:
        print(f"Saving {product.name} from {product.abs_href}...")
        crawler.save_product(product, output_path, use_cache=False)
        print(f"Saving {product.name} FAQ from {product.abs_href_faq}...")
        crawler.save_faq(product, output_path, use_cache=False)

    print("Finished.")


def run_aws_crawler_examples():
    logging.info("Example 1: List AWS products")
    from cloud_products.aws import AwsCrawler

    for product in AwsCrawler().get_products():
        print(f"{product.code}: {product.name}: {product.desc}")

    logging.info("Example 2: Get product descriptions as a list of lines")
    from cloud_products.aws import AwsCrawler

    crawler = AwsCrawler()
    print(crawler)
    product = crawler.get_products()[0]
    lines = crawler.get_product_text(product)
    print(lines[4])

    logging.info("Example 3: Get matching product(s)")
    from cloud_products.aws import AwsCrawler

    crawler = AwsCrawler()
    sagemaker_products = crawler.get_products_matching("sagemaker")
    sagemaker_description = crawler.get_product_text(sagemaker_products[0])
    print(sagemaker_description[3])

    logging.info("Example 4: Save product descriptions and FAQ pages to files:")
    from cloud_products.aws import AwsCrawler

    for product in AwsCrawler().get_products()[0:5]:
        print(f"Saving {product.name} from {product.abs_href}...")
        crawler.save_product(product, output_path)
        crawler.save_faq(product, output_path)

    logging.info("Example 5: Convert list of products to Pandas dataframe")
    import pandas as pd
    from cloud_products.aws import AwsCrawler

    products = AwsCrawler().get_products()
    df = pd.DataFrame.from_records([vars(p) for p in products])
    print(df)

    logging.info("Example 6: Get Pandas dataframe of products:")
    from cloud_products.aws import AwsCrawler

    df = AwsCrawler().get_products_as_df(use_cache=True)
    print(df.columns)
    print(df)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    vendor = "aws"
    output_path = "./_data/scrape_results/"

    run_type = "full"
    # run_type = "examples"

    if vendor == "aws" and run_type == "full":
        run_full_aws_crawler()

    elif vendor == "aws" and run_type != "full":
        run_aws_crawler_examples()

    elif vendor == "gcp":
        raise Exception("Google Cloud Compute not currently supported")

    elif vendor == "azure":
        raise Exception("Microsoft Azure not currently supported")

    else:
        raise Exception(f"Unknown vendor {vendor}")
