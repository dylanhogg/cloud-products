# cloud-products 

A package for getting cloud products and product descriptions from a cloud provider website.

Currently supports AWS only, being the products listed at 
[https://aws.amazon.com/products](https://aws.amazon.com/products)

Usage to get product descriptions as a list of lines:
```
from crawler import aws
crawler = aws.AwsCrawler()
for product in crawler.get_products():
    lines = crawler.get_product_text(product)
```

Usage to save product descriptions to files:
```
from crawler import aws
crawler = aws.AwsCrawler()
for product in crawler.get_products():
    crawler.save_product(product, output_path)
```

Usage to get matching product(s):
```
from crawler import aws
crawler = aws.AwsCrawler()
sagemaker_products = crawler.get_products_matching("sagemaker")
sagemaker_description = crawler.get_product_text(sagemaker_products[0])
```

Cloud Products is distributed under the MIT license.
